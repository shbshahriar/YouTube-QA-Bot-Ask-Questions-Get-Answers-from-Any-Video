import os
from dotenv import load_dotenv
from video_processor import process_video
from ui_utils import print_header, print_menu, print_help, print_chat_start

# Load environment variables
load_dotenv()

# Check for API key
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in .env file. Please add your API key.")

def main():
    while True:
        print_header()
        print_menu()
        
        choice = input("\nEnter your choice (1-2): ")
        
        if choice == "1":
            video_url = input("\nEnter YouTube video URL: ")
            try:
                qa_chain = process_video(video_url)
                print_chat_start()
                
                # Ask questions
                while True:
                    query = input("\nYou: ")
                    if query.lower() == 'quit':
                        return
                    elif query.lower() == 'back':
                        break
                    elif query.lower() == 'help':
                        print_help()
                        continue
                        
                    try:
                        response = qa_chain.invoke({"question": query})
                        print("\nBot:", response['answer'])
                    except Exception as e:
                        print(f"\nError getting response: {str(e)}")
                    
            except Exception as e:
                print(f"Error: {str(e)}")
                
        elif choice == "2":
            print("\nGoodbye!")
            break
            
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
