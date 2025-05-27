def print_header():
    """Print the application header."""
    print("\n" + "="*50)
    print("YouTube QA Bot")
    print("="*50)

def print_menu():
    """Print the main menu options."""
    print("1. Process new video")
    print("2. Exit")

def print_help():
    """Print help message for navigation."""
    print("\nNavigation commands:")
    print("- Type 'back' to process another video")
    print("- Type 'quit' to exit the program")
    print("- Type 'help' to see this message again")

def print_chat_start():
    """Print chat session start message."""
    print("\nChat session started! You can now ask questions about the video.")
    print("The bot will remember our conversation context.")
    print_help() 