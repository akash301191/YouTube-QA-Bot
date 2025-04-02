# YouTube QA Bot

YouTube QA Bot is an intuitive Streamlit application that lets you paste a YouTube video URL, have a conversation with a bot about the video's content, and download a transcript of your interaction. Powered by the [Embedchain](https://github.com/embedchain/embedchain) library and OpenAI's GPT-4 model, this tool makes it simple to explore and discuss the content of YouTube videos.

## Folder Structure

```
YouTube-QA-Bot/
├── youtube-qa-bot.py
├── README.md
└── requirements.txt
```

- **youtube-qa-bot.py**: The main Streamlit application.
- **requirements.txt**: A list of all required Python packages.
- **README.md**: This documentation file.

## Features

- **YouTube URL Input:** Paste a YouTube video URL to fetch its transcript and add it to a knowledge base.
- **Video Summary:** Automatically generate a concise summary of the video once the transcript is added.
- **Conversational Q&A:** Ask questions about the video content and receive responses in real time.
- **Transcript Download:** Save the entire conversation as a text file.
- **Streamlined Interface:** A clean interface built with Streamlit.

## Prerequisites

- Python 3.11 or higher
- An OpenAI API key (get yours [here](https://platform.openai.com/account/api-keys))

## Installation

1. **Clone the repository** (or download it):
   ```bash
   git clone https://github.com/yourusername/YouTube-QA-Bot.git
   cd YouTube-QA-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit app**:
   ```bash
   streamlit run youtube-qa-bot.py
   ```
2. **Open your browser** to the local URL shown in the terminal (usually `http://localhost:8501`).
3. **Interact with the app**:
   - Enter your OpenAI API key when prompted.
   - Paste a YouTube video URL.
   - View the generated video summary.
   - Ask questions about the video content.
   - Download the transcript of your conversation if needed.

## Code Overview

- **`create_embedchain_bot`**: Initializes the Embedchain bot with OpenAI GPT-4 and a Chroma vector database.
- **`extract_video_id` & `fetch_video_data`**: Retrieve the transcript (and a placeholder title) from a provided YouTube URL.
- **`add_video_to_knowledge_base`**: Adds the video transcript to the bot’s knowledge base.
- **`generate_video_summary`**: Generates and stores a concise summary of the video transcript.
- **`ask_question`**: Manages user input, queries the bot, and displays the answer while appending the Q&A pairs to a conversation transcript.
- **`download_transcript`**: Provides a download button for saving the conversation transcript as a text file.
- **`main`**: Orchestrates the overall Streamlit app workflow—from capturing the API key and YouTube URL to generating a summary and handling the Q&A session.

## Contributions

Contributions are welcome! Feel free to fork the repository, improve the code, and open a pull request. Please ensure that your changes follow the existing style and include any necessary documentation or tests.