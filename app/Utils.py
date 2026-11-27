# Shared settings and helpers, used by more than one file
# Imports nothing from the project, so any file can import it without a circular import

import os

# The score file's name, defined once so the game and the web server can't drift apart
SCORES_FILE_NAME = "Scores.txt"

# The repo root, found from this file's own location (app/Utils.py → two levels up), never from
# the folder a program was started in
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The score file's full path, shared by the game and the web server (task 8).
# The WOG_SCORES_FILE_PATH env var wins if it's set (Docker sets /Scores.txt); empty counts as not set
SCORES_FILE_PATH = os.environ.get("WOG_SCORES_FILE_PATH") or os.path.join(_REPO_ROOT, SCORES_FILE_NAME)

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
