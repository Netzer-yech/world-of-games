# Exact decimal math for money, its input error, and the rounding rule
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

# HTTP package for calling the currency API (from requirements.txt)
import requests

# The API address; uppercase = a constant that never changes
API_URL = "https://open.er-api.com/v6/latest/USD"


# Get today's USD to ILS rate from the API, or None if anything fails
def get_usd_to_ils_rate():
    # Anything that fails inside try jumps to except instead of crashing
    try:
        # Send the GET request; give up if there's no answer within 5 seconds
        response = requests.get(API_URL, timeout=5)
        # Turn an HTTP error status (like 404 or 500) into an exception
        response.raise_for_status()
        # Turn the JSON text into a Python dictionary
        data = response.json()
        # The API reports its own status; anything but "success" = no rate
        if data["result"] != "success":
            return None
        # Take the ILS value from inside the "rates" section
        return data["rates"]["ILS"]
    # Network error, timeout, bad HTTP status, invalid JSON, or a missing key
    except (requests.RequestException, ValueError, KeyError):
        return None


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
        # A real number (not NaN/Infinity) and not negative
        if guess.is_finite() and guess >= 0:
             # Round to agorot, the same rounding as the correct answer
            return guess.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        # Negative or not a real number: explain, then ask again
        print("Please enter a number of 0 or more, like 145 or 145.50.")