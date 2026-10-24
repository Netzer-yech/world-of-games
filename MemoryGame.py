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