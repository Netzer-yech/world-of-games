# Python's built-in module for random numbers
import random


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