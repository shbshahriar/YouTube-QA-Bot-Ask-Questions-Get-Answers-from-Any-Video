from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import re
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Set seed for consistent language detection
DetectorFactory.seed = 0

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats."""
    # Handle youtu.be URLs
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    
    # Handle youtube.com URLs
    if "youtube.com" in url:
        # Try to get video ID from query parameters
        parsed_url = urlparse(url)
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query).get("v", [None])[0]
        elif parsed_url.path.startswith("/embed/"):
            return parsed_url.path.split("/")[2]
        elif parsed_url.path.startswith("/live/"):
            return parsed_url.path.split("/")[2]
    
    # Try to find video ID using regex as fallback
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    if video_id_match:
        return video_id_match.group(1)
    
    return None

def verify_english_text(text, sample_size=1000):
    """Verify if the text is in English."""
    # Take a sample of the text for language detection
    sample = text[:sample_size] if len(text) > sample_size else text
    
    try:
        # Try multiple times with different samples for more accuracy
        for i in range(3):
            start = i * (len(sample) // 3)
            end = start + (len(sample) // 3)
            sample_text = sample[start:end]
            
            if sample_text.strip():
                lang = detect(sample_text)
                if lang != 'en':
                    return False, lang
    except LangDetectException:
        return False, "unknown"
    
    return True, "en"

def get_transcript(video_url):
    """Get transcript for a YouTube video."""
    try:
        video_id = extract_video_id(video_url)
        if not video_id:
            raise ValueError(f"Could not extract video ID from URL: {video_url}")
        
        # Try to get English transcript first
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        except (TranscriptsDisabled, NoTranscriptFound):
            raise ValueError("No English transcript available for this video. Please try a video with English captions.")
        
        # Combine all transcript text
        full_text = " ".join([t['text'] for t in transcript])
        
        # Verify the text is in English
        is_english, detected_lang = verify_english_text(full_text)
        if not is_english:
            raise ValueError(f"Video transcript appears to be in {detected_lang.upper()}. Only English transcripts are supported.")
            
        return full_text
        
    except Exception as e:
        if isinstance(e, ValueError):
            raise e
        raise ValueError(f"Error getting transcript: {str(e)}")
