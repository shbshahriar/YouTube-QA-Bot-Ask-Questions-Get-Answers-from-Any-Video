# YouTube QA Bot

A powerful tool that allows you to ask questions about YouTube videos and get accurate answers based on the video's content using Google's Generative AI. The bot maintains conversation context and ensures English-only transcripts for optimal performance.

## Features

- Extract and process English transcripts from YouTube videos
- Automatic language detection and verification
- Process and store video content in a vector database (ChromaDB)
- Ask questions about the video content using Google's Gemini Pro model
- Interactive question-answering interface with conversation memory
- Automatic database management to avoid duplicates
- Clear navigation and help system

## Setup

1. Clone this repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Unix/MacOS
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory and add your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

1. Run the main script:
   ```bash
   python main.py
   ```
2. Choose option 1 to process a new video
3. Enter a YouTube video URL (must have English captions)
4. The script will:
   - Verify the video has English captions
   - Process the video transcript
   - Create a fresh vector database
   - Start an interactive Q&A session
5. Ask questions about the video content
6. Use navigation commands:
   - Type 'back' to process another video
   - Type 'quit' to exit the program
   - Type 'help' to see navigation options

## Project Structure

- `main.py`: Main entry point with interactive Q&A interface
- `transcript_utils.py`: Utilities for handling YouTube video transcripts and language detection
- `vector_store.py`: Vector database management using ChromaDB
- `qa_chain.py`: Question-answering implementation using Google's Gemini Pro
- `video_processor.py`: Video processing and QA chain setup
- `ui_utils.py`: User interface and navigation functions
- `requirements.txt`: Project dependencies
- `README.md`: Project documentation

## Dependencies

- Python 3.8+
- Google API key (for Gemini Pro and embeddings)
- Internet connection for YouTube video access
- Required Python packages (see requirements.txt)

## How It Works

1. **Transcript Extraction**: 
   - Gets the video transcript using youtube-transcript-api
   - Verifies English language using langdetect
   - Ensures only English content is processed

2. **Text Processing**: 
   - Splits the transcript into manageable chunks
   - Creates embeddings for semantic search

3. **Vector Storage**: 
   - Stores the chunks in ChromaDB with embeddings
   - Automatically manages database to avoid duplicates
   - Creates fresh database for each video

4. **Question Answering**: 
   - Uses Google's Gemini Pro for natural language understanding
   - Maintains conversation context for follow-up questions
   - Provides accurate answers based on video content

## Notes

- Only English videos with captions are supported
- Each video creates a fresh database to ensure clean context
- The system uses Google's text-embedding-004 model for embeddings
- Questions are answered using Google's Gemini Pro model
- Conversation memory is maintained during the Q&A session
- Database is automatically cleared when processing new videos

## Error Handling

The system includes robust error handling for:
- Invalid YouTube URLs
- Missing or non-English transcripts
- Database access issues
- API errors
- Language detection problems

## License

MIT License 