
# The three game modules; each one has play(difficulty)
import CurrencyRouletteGame
import GuessGame
import MemoryGame


# welcome function that accept user input and return welcome text
def welcome(name):                                                        
    return f"\nHello {name} and welcome to the World of Games (WoG).\nHere you can find many cool games to play."


# Ask the player for a number, and keep asking until it is valid.
# prompt = the question text, low/high = smallest and biggest allowed number.
def get_number(prompt, low, high):
    # Repeat forever. The only exit is "return" below, reached with valid input.
    while True:
        # Show the question and wait for Enter. The answer is always text (a string).
        answer = input(prompt)
        # "try" = attempt the next line. If it fails, jump to "except" instead of crashing.
        try:
            # Turn the text into a whole number: "3" -> 3.
            # Fails on "", "abc", "2.5" with an error called ValueError.
            number = int(answer)
        # Runs only if int() failed with ValueError.
        except ValueError:
            # Tell the player what was wrong. {answer} inserts what they typed.
            print(f"'{answer}' is not a whole number, please try again.")
            # Skip the rest of the loop and go back to the top: ask again.
            continue
        # We get here only with a whole number. Check that it's inside the range.
        # Same as: low <= number AND number <= high. The endpoints are allowed.
        if low <= number <= high:
            # Valid: send the number back to the caller, and leave the loop and the function.
            return number
        # Whole number but out of range: explain, then the loop asks again.
        print(f"Please choose a number from {low} to {high}.")


# Show the game menu
def load_game():
    print("\nPlease choose a game to play:\n")
    print("1. Memory Game - a sequence of numbers will appear for 0.7 seconds, repeat it back")
    print("2. Guess Game - guess the secret number the computer chose")
    print("3. Currency Roulette - guess the ILS value of a random USD amount\n")
    # Ask for the game number, check with range 1-3
    game = get_number("Enter game number (1-3): ", 1, 3)
    # Ask for the difficulty, same check with range 1-5
    difficulty = get_number("Please choose game difficulty from 1 to 5: ", 1, 5)
    # Start the chosen game with the chosen difficulty
    if game == 1:
        result = MemoryGame.play(difficulty)
    elif game == 2:
        result = GuessGame.play(difficulty)
    else:
        result = CurrencyRouletteGame.play(difficulty)
    # Same result message for every game
    if result:
        print("You won!")
    else:
        print("You lost, better luck next time.")