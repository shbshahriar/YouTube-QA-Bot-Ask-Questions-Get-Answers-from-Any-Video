from transcript_utils import get_transcript
from vector_store import create_vector_store
from qa_chain import build_qa_chain

def process_video(video_url):
    """Process a YouTube video and return the QA chain."""
    print(f"\nProcessing video: {video_url}")
    
    # Get transcript
    transcript = get_transcript(video_url)
    if not transcript:
        raise ValueError("Could not get transcript for the video")
    
    # Create vector store
    print("\nCreating vector store...")
    vector_db = create_vector_store(transcript)
    
    # Build QA chain
    print("\nBuilding QA chain...")
    return build_qa_chain(vector_db) 