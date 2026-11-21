# Shared settings and helpers, used by more than one file
# Imports nothing from the project, so any file can import it without a circular import

import os

# The score file's name, defined once so the game and the web server can't drift apart
SCORES_FILE_NAME = "Scores.txt"

# Returned instead of a score when it can't be read or saved.
# A real score is a whole number of 0 or more, so -1 can never be mistaken for one;
# 0 would look like a real new-player score and hide the error.
BAD_RETURN_CODE = -1


# Named in PEP 8 style (the brief writes it Screen_cleaner); shared, so any game can clear the screen
def screen_cleaner():
    # Windows ("nt") and Linux/macOS use different commands
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
