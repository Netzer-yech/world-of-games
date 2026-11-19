import random


# Pick the secret number; randint includes both ends, so 1 and difficulty are both possible
def generate_number(difficulty):
    secret_number = random.randint(1, difficulty)
    return secret_number


# Ask until the guess is a whole number from 1 to difficulty
def get_guess_from_user(difficulty):
    while True:
        answer = input(f"Guess a number from 1 to {difficulty}: ")
        try:
            guess = int(answer)
        # A typo isn't a wrong guess: explain and ask again instead of losing the round
        except ValueError:
            print(f"'{answer}' is not a whole number, please try again.")
            continue
        # The secret is always 1 to difficulty, so a number outside it is a typo too
        if 1 <= guess <= difficulty:
            return guess
        print(f"Please choose a number from 1 to {difficulty}.")


# True only on an exact match
def compare_results(secret_number, guess):
    return secret_number == guess


# Run one round: True = win, False = loss
def play(difficulty):
    print("Guess Game: guess the secret number!")
    secret_number = generate_number(difficulty)
    guess = get_guess_from_user(difficulty)
    # Reveal the number only after the guess, so it can't help the player
    print(f"The secret number was {secret_number}.")
    return compare_results(secret_number, guess)