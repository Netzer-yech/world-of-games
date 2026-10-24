# Run terminal commands and check the operating system
import os
# Python's built-in module for random numbers
import random
# Pause the program for a number of seconds
import time


# Make a list of difficulty random numbers, each from 1 to 101
def generate_sequence(difficulty):
    # Start with an empty list
    sequence = []
    # Repeat the indented line difficulty times
    for _ in range(difficulty):
        # Add one random number (1 to 101) to the end of the list
        sequence.append(random.randint(1, 101))
    # Give the full list back
    return sequence


# Clear the terminal screen (moves to Utils.py in Part 2)
def clear_screen():
    # os.name is "nt" on Windows, which uses "cls"
    if os.name == "nt":
        os.system("cls")
    # Linux and macOS use "clear"
    else:
        os.system("clear")


# Show the sequence for 0.7 seconds, then hide it
def display_sequence(sequence):
    # Show the numbers to the player
    print(f"Remember this sequence: {sequence}")
    # Wait 0.7 seconds
    time.sleep(0.7)
    # Wipe the screen so the numbers can't be read anymore
    clear_screen()


# Ask until the player enters exactly difficulty whole numbers
def get_list_from_user(difficulty):
    # Repeat until "return" is reached with a valid list
    while True:
        # Explain the format, then read the whole line as text
        answer = input(f"Enter the {difficulty} numbers you saw, separated by spaces: ")
        # split() cuts the text at the spaces: "12 7 12" -> ["12", "7", "12"]
        parts = answer.split()
        # len() counts the items. Wrong count -> explain and ask again
        if len(parts) != difficulty:
            print(f"Please enter exactly {difficulty} numbers.")
            continue
        # Start an empty list for the converted numbers
        numbers = []
        # Try to turn every part into a whole number
        try:
            # Go over the parts one by one
            for part in parts:
                # Convert the text to a number and add it to the list
                numbers.append(int(part))
        # One part was not a whole number, e.g. "abc" or "2.5"
        except ValueError:
            print("Please use whole numbers only, separated by spaces.")
            continue
        # Count and values are valid: give the list back
        return numbers


# True only if both lists have the same numbers in the same order
def is_list_equal(list1, list2):
    # == on lists compares item by item, position by position
    return list1 == list2


