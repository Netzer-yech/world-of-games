
# welcome function that accept user input and return welcome text
def welcome(name):                                                        
    return f"\nHello {name} and welcome to the World of Games (WoG).\nHere you can find many cool games to play."


# Show the game menu
def load_game():
    print("\nPlease choose a game to play:\n")
    print("1. Memory Game - a sequence of numbers will appear for 0.7 seconds, repeat it back")
    print("2. Guess Game - guess the secret number the computer chose")
    print("3. Currency Roulette - guess the ILS value of a random USD amount\n")