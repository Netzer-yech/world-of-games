import os
import random
import time


# The sequence's number range; generating and checking both use it, so they can't disagree
LOWEST_NUMBER = 1
HIGHEST_NUMBER = 101


# Make a list of difficulty random numbers inside the allowed range
def generate_sequence(difficulty):
    sequence = []
    for _ in range(difficulty):
        sequence.append(random.randint(LOWEST_NUMBER, HIGHEST_NUMBER))
    return sequence


# Clear the terminal screen (moves to Utils.py in Part 2)
def clear_screen():
    # Windows ("nt") and Linux/macOS use different commands
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


# Show the sequence for 0.7 seconds (the brief's rule), then hide it
def display_sequence(sequence):
    print(f"Remember this sequence: {sequence}")
    time.sleep(0.7)
    # Wipe the screen so the numbers can't be read back
    clear_screen()


# Ask until the player enters exactly difficulty whole numbers from the allowed range
def get_list_from_user(difficulty):
    while True:
        answer = input(f"Enter the {difficulty} numbers you saw, separated by spaces: ")
        # split() with no argument also ignores extra spaces around and between numbers
        parts = answer.split()
        # Each check below rejects one kind of typo and asks again, instead of losing the round
        if len(parts) != difficulty:
            print(f"Please enter exactly {difficulty} numbers.")
            continue
        numbers = []
        try:
            for part in parts:
                numbers.append(int(part))
        except ValueError:
            print("Please use whole numbers only, separated by spaces.")
            continue
        # The sequence only uses this range, so a number outside it is a typo, not a wrong answer
        if not all(LOWEST_NUMBER <= number <= HIGHEST_NUMBER for number in numbers):
            print(f"Please use numbers from {LOWEST_NUMBER} to {HIGHEST_NUMBER} only.")
            continue
        return numbers


# True only if both lists have the same numbers in the same order
def is_list_equal(list1, list2):
    return list1 == list2


# Run one round: True = win, False = loss
def play(difficulty):
    print("Memory Game: remember the numbers!")
    sequence = generate_sequence(difficulty)
    display_sequence(sequence)
    user_list = get_list_from_user(difficulty)
    # Reveal the sequence only after the answer, so it can't help the player
    print(f"The sequence was {sequence}.")
    return is_list_equal(sequence, user_list)