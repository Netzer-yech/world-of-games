# Python's built-in module for random numbers
import random


# Pick a random whole number from 1 to difficulty, both included
def generate_number(difficulty):
    # randint(a, b) returns a random whole number, a and b are both possible
    secret_number = random.randint(1, difficulty)
    # Give the number back to whoever called the function
    return secret_number