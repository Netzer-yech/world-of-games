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