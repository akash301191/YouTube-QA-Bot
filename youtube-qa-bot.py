import tempfile
import streamlit as st
from embedchain import App
from youtube_transcript_api import YouTubeTranscriptApi
from typing import Tuple

def create_embedchain_bot(db_path: str, api_key: str) -> App:
    """
    Initialize the EmbedChain bot with the given database path and OpenAI API key.
    """
    config = {
        "llm": {
            "provider": "openai", 
            "config": {
                "model": "gpt-4", 
                "temperature": 0.5, 
                "api_key": api_key
            }
        },
        "vectordb": {
            "provider": "chroma", 
            "config": {"dir": db_path}
        },
        "embedder": {
            "provider": "openai", 
            "config": {"api_key": api_key}
        }
    }
    return App.from_config(config=config)

def extract_video_id(video_url: str) -> str:
    """
    Extract the YouTube video ID from the provided URL.
    """
    if "youtube.com/watch?v=" in video_url:
        return video_url.split("v=")[-1].split("&")[0]
    elif "youtube.com/shorts/" in video_url:
        return video_url.split("/shorts/")[-1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL")

def fetch_video_data(video_url: str) -> Tuple[str, str]:
    """
    Fetch the transcript (and a placeholder title) for a given YouTube video URL.
    """
    try:
        video_id = extract_video_id(video_url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry["text"] for entry in transcript])
        # For simplicity, we're using "Unknown" as the title.
        return "Unknown", transcript_text
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return "Unknown", "No transcript available for this video."

def add_video_to_knowledge_base(app: App, video_url: str) -> str:
    """
    Fetch video data and add it to the bot's knowledge base.
    Returns the transcript if added, or an empty string otherwise.
    """
    title, transcript = fetch_video_data(video_url)
    if transcript != "No transcript available for this video":
        app.add(transcript, data_type="text", metadata={"title": title, "url": video_url})
        st.success(f"Added video '{title}' to knowledge base")
        return transcript
    else:
        st.warning(f"No transcript available for video '{title}'. Cannot add to knowledge base.")
        return ""

def generate_video_summary(app: App, transcript: str) -> None:
    """
    Generate a video summary if not already generated, and display it.
    """
    if "video_summary" not in st.session_state:
        with st.spinner("Generating video summary..."):
            summary_prompt = f"Provide a concise summary for the following video transcript:\n\n{transcript}"
            summary = app.chat(summary_prompt)
        st.session_state.video_summary = summary
    st.markdown(st.session_state.video_summary)

def ask_question(app: App) -> None:
    """
    Prompts the user to ask a question about the YouTube video, displays the answer,
    and stores the conversation transcript (user-bot Q&A) in session state.
    """
    query = st.text_input("Ask any question about the YouTube Video")
    if query:
        try:
            answer = app.chat(query)
            st.markdown(answer)
            # Initialize conversation transcript if not already present
            if "conversation_transcript" not in st.session_state:
                st.session_state.conversation_transcript = ""
            # Append Q&A pair to the conversation transcript
            st.session_state.conversation_transcript += f"Query: {query}\nResponse: {answer}\n\n"
        except Exception as e:
            st.error(f"Error chatting with the video: {e}")

def download_transcript() -> None:
    """
    Provides a download button for the conversation transcript.
    """
    conversation_transcript = st.session_state.get("conversation_transcript", "")
    if conversation_transcript:
        st.download_button(
            label="Download Conversation Transcript",
            data=conversation_transcript,
            file_name="youtube-qa-conversation-transcript.txt",
            mime="text/plain"
        )

def main() -> None:
    """
    Main function to run the YouTube QA Bot.
    """
    st.set_page_config(page_title="YouTube QA Bot")
    
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 0rem !important;
            padding-right: 0rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1 style='font-size: 2.5rem;'>📺 YouTube QA Bot</h1>", unsafe_allow_html=True)
    st.markdown("Welcome to YouTube QA Bot — an intuitive tool to interactively explore and discuss YouTube videos")
    st.markdown("<br>", unsafe_allow_html=True)

    # Get the OpenAI API key
    openai_access_token = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if not openai_access_token:
        return

    # Create a temporary directory for the database and initialize the bot
    db_path = tempfile.mkdtemp()
    app = create_embedchain_bot(db_path, openai_access_token)
    
    # Prompt for YouTube Video URL and add it to the knowledge base
    video_url = st.text_input("Enter YouTube Video URL")
    transcript = ""
    if video_url:
        try:
            transcript = add_video_to_knowledge_base(app, video_url)
        except Exception as e:
            st.error(f"Error adding video: {e}")

    # If a transcript was successfully added, generate a summary only once, then prompt for questions
    if transcript:
        st.markdown("<br>", unsafe_allow_html=True)
        generate_video_summary(app, transcript)
        st.markdown("<br>", unsafe_allow_html=True)
        ask_question(app)
    
    # Provide option to download the conversation transcript
    download_transcript()

if __name__ == "__main__":
    main()