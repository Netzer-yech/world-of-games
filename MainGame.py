# The entry point of World of Games
from Live import welcome, load_game

# Run only when this file is started directly, not when it's imported (e.g. by tests)
if __name__ == "__main__":
    # Ctrl+C or Ctrl+D anywhere in the game travels up to here
    try:
        name = input("Please enter your name: ")
        print(welcome(name))
        load_game()
    # The player chose to quit: say goodbye instead of showing a traceback
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")