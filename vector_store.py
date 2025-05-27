from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import os
import shutil
import logging
import time
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def clear_database(persist_directory="db"):
    """Clear the existing database directory with retry mechanism."""
    if not os.path.exists(persist_directory):
        return

    max_retries = 3
    retry_delay = 1  # seconds

    for attempt in range(max_retries):
        try:
            # First try to remove individual files
            for root, dirs, files in os.walk(persist_directory, topdown=False):
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                    except Exception as e:
                        logger.warning(f"Could not remove file {name}: {str(e)}")
                
                for name in dirs:
                    try:
                        os.rmdir(os.path.join(root, name))
                    except Exception as e:
                        logger.warning(f"Could not remove directory {name}: {str(e)}")
            
            # Then try to remove the main directory
            try:
                shutil.rmtree(persist_directory)
                logger.info("Cleared existing database")
                return
            except Exception as e:
                logger.warning(f"Could not remove directory {persist_directory}: {str(e)}")
                
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                
        except Exception as e:
            logger.error(f"Error clearing database (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
    
    # If we couldn't clear the directory, create a new one with a timestamp
    timestamp = int(time.time())
    new_directory = f"{persist_directory}_{timestamp}"
    logger.info(f"Creating new database directory: {new_directory}")
    return new_directory

def create_vector_store(transcript, persist_directory="db", collection_name="youtube_transcripts"):
    """Create or update vector store with transcript."""
    # Clear existing database and get new directory if needed
    new_directory = clear_database(persist_directory)
    if new_directory:
        persist_directory = new_directory
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = splitter.split_text(transcript)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # Create new collection with the texts
    vectordb = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name
    )
    
    print(f"Created vector store with {len(texts)} chunks")
    return vectordb
