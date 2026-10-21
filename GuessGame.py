# Python's built-in module for random numbers
import random


# Pick a random whole number from 1 to difficulty, both included
def generate_number(difficulty):
    # randint(a, b) returns a random whole number, a and b are both possible
    secret_number = random.randint(1, difficulty)
    # Give the number back to whoever called the function
    return secret_number

# Ask the player for a guess from 1 to difficulty, until it is valid
def get_guess_from_user(difficulty):
    # Repeat until "return" is reached with a valid guess
    while True:
        # Show the question and read the answer as text
        answer = input(f"Guess a number from 1 to {difficulty}: ")
        # Try to turn the text into a whole number
        try:
            guess = int(answer)
        # int() failed: empty, text or a fraction
        except ValueError:
            print(f"'{answer}' is not a whole number, please try again.")
            # Go back to the top of the loop and ask again
            continue
        # Whole number: check it is inside the range, endpoints included
        if 1 <= guess <= difficulty:
            # Valid: give the guess back and stop asking
            return guess
        # Out of range: explain, then the loop asks again
        print(f"Please choose a number from 1 to {difficulty}.")

# Return True if the guess matches the secret number, otherwise False
def compare_results(secret_number, guess):
    # == compares two values and gives True or False
    return secret_number == guess

# Run one round of the Guess Game: True = win, False = loss
def play(difficulty):
    # Show which game started
    print("Guess Game: guess the secret number!")
    # Pick the secret number, without showing it
    secret_number = generate_number(difficulty)
    # Ask until the player gives one valid guess
    guess = get_guess_from_user(difficulty)
    # Reveal the number only after the guess
    print(f"The secret number was {secret_number}.")
    # Compare, and send True or False back to the caller
    return compare_results(secret_number, guess)