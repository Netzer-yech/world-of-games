# The three game modules; each one has play(difficulty)
import CurrencyRouletteGame
import GuessGame
import MemoryGame


# Return the greeting instead of printing it, so the caller decides when to show it
def welcome(name):
    return f"\nHello {name} and welcome to the World of Games (WoG).\nHere you can find many cool games to play."


# Ask for the player's name until it isn't empty
def get_name():
    while True:
        # strip() so "  Netzer " greets as "Netzer", and "   " counts as empty
        name = input("Please enter your name: ").strip()
        if name:
            return name
        print("Please enter a name.")


# Ask until the answer is a whole number from low to high; shared by the game and difficulty menus
def get_number(prompt, low, high):
    while True:
        answer = input(prompt)
        try:
            number = int(answer)
        # A typo isn't a choice: explain and ask again instead of crashing
        except ValueError:
            print(f"'{answer}' is not a whole number, please try again.")
            continue
        # Both ends are valid choices
        if low <= number <= high:
            return number
        print(f"Please choose a number from {low} to {high}.")


# Show the menu, run the chosen game, and print its result
def load_game():
    print("Please choose a game to play:")
    print("1. Memory Game - a sequence of numbers will appear for 0.7 seconds, repeat it back")
    print("2. Guess Game - guess the secret number the computer chose")
    print("3. Currency Roulette - guess the ILS value of a random USD amount")

    # get_number asks again until the answer is in range, so both values are always valid
    game = get_number("Enter game number (1-3): ", 1, 3)
    difficulty = get_number("Please choose game difficulty from 1 to 5: ", 1, 5)
    # A game raises RoundCancelledError when the round can't be played
    try:
        if game == 1:
            result = MemoryGame.play(difficulty)
        elif game == 2:
            result = GuessGame.play(difficulty)
        else:
            result = CurrencyRouletteGame.play(difficulty)
    # Cancelled is neither a win nor a loss: show why, and skip the result message
    except CurrencyRouletteGame.RoundCancelledError as error:
        print(error)
        return

    # One result message for every game
    if result:
        print("You won!")
    else:
        print("You lost, better luck next time.")