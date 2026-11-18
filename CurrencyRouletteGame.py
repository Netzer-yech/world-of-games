# Exact decimal math for money, its input error, and the rounding rule
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
# isfinite() rejects NaN and infinity in the API rate
import math
# Python's built-in module for random numbers
import random

# HTTP package for calling the currency API (from requirements.txt)
import requests


# The highest guess accepted: far above any real answer, small enough to round safely
MAX_GUESS = Decimal("1000000")
# The API address; uppercase = a constant that never changes
API_URL = "https://open.er-api.com/v6/latest/USD"


# Get today's USD to ILS rate, or None if the API answer can't be used
def get_usd_to_ils_rate():
    # try holds only what can fail unpredictably: the network and the JSON parsing
    try:
        # timeout=5 so a slow API can't freeze the game
        response = requests.get(API_URL, timeout=5)
        # A 404 or 500 page is not a rate
        response.raise_for_status()
        data = response.json()
    # Network error, timeout, bad HTTP status, or a body that isn't JSON
    except (requests.RequestException, ValueError):
        return None
    # Valid JSON can be null, a list or a number; only an object has our fields
    if not isinstance(data, dict) or data.get("result") != "success":
        return None
    # "rates" may be missing or null; .get() gives None instead of a KeyError
    rates = data.get("rates")
    if not isinstance(rates, dict):
        return None
    rate = rates.get("ILS")
    # bool is a kind of int in Python, so true would pass as a rate of 1
    if isinstance(rate, bool) or not isinstance(rate, (int, float)):
        return None
    # The teacher's rule: a real, positive number (no NaN, infinity, 0 or below)
    if not math.isfinite(rate) or rate <= 0:
        return None
    return rate

# Return the lowest and highest winning answers, in ILS, rounded to 2 places
def get_money_interval(usd_amount, rate, difficulty):
    # str() first, so the float's binary noise doesn't enter the Decimal
    exact_rate = Decimal(str(rate))
    # t = the correct ILS amount, rounded to 2 places (agorot)
    t = (Decimal(usd_amount) * exact_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    # Allowed distance from t: difficulty 1 -> 4, difficulty 5 -> 0
    margin = Decimal(5 - difficulty)
    # Return both bounds together
    return t - margin, t + margin


# Ask until the player enters a number of 0 or more, like 145 or 145.50
def get_guess_from_user(usd_amount):
    # Repeat until "return" is reached with a valid guess
    while True:
        # Show only the USD amount, never the rate or the answer
        answer = input(f"How many ILS is {usd_amount} USD? ")
        # Try to turn the text into an exact Decimal
        try:
            guess = Decimal(answer)
        # Not a number: empty, text, "1,000"...
        except InvalidOperation:
            print("Please enter a number, like 145 or 145.50.")
            continue
        # Real, not negative, and not too big to round (1e100 crashed quantize)
        if guess.is_finite() and 0 <= guess <= MAX_GUESS:
            # Same rounding as the correct answer, so the comparison is fair
            return guess.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        print(f"Please enter a number from 0 to {MAX_GUESS}, like 145 or 145.50.")


# Run one round of Currency Roulette: True = win, False = loss or cancelled
def play(difficulty):
    # Show which game started
    print("Currency Roulette: guess the ILS value of a USD amount!")
    # Get the rate once; the whole round uses this same rate
    rate = get_usd_to_ils_rate()
    # No rate = cancel the round before asking anything, never a win
    if rate is None:
        print("Could not get today's exchange rate, the round is cancelled.")
        return False
    # Random whole USD amount, 1 to 100 included
    usd_amount = random.randint(1, 100)
    # Unpack the two returned bounds into two variables
    lower, upper = get_money_interval(usd_amount, rate, difficulty)
    # Ask until the player gives a valid guess (already rounded to agorot)
    guess = get_guess_from_user(usd_amount)
    # Reveal the winning range only after the guess
    print(f"Winning answers were {lower} to {upper} ILS.")
    # True if the guess is inside the range, endpoints included
    return lower <= guess <= upper