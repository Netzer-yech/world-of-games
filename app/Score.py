# The scoring layer: the only code that reads or writes the score,
# so Part 3 can swap the file for a database without touching the games or the web server
import os

from Utils import SCORES_FILE_NAME, SCORES_FILE_PATH, BAD_RETURN_CODE


# Raised when the score can't be read or saved; its message is shown to the player or on the web page
class ScoreError(Exception):
    pass


# Return the saved score; raise ScoreError when the file exists but can't be trusted.
# missing_ok: a missing file is a first game (0) for the console, but an error for the web page
def read_score(missing_ok=True):
    try:
        # Explicit encoding: the default differs between Windows and Linux
        with open(SCORES_FILE_PATH, encoding="utf-8") as file:
            text = file.read()
    # No file yet: the console's first game ("start from zero"); for the web it means missing data
    except FileNotFoundError:
        if missing_ok:
            return 0
        raise ScoreError(f"No score found: {SCORES_FILE_NAME} does not exist.")
    # The file is there but can't be read (no permission, a folder, a disk error): never treat it as 0
    except OSError as error:
        raise ScoreError(f"Could not read {SCORES_FILE_NAME}: {error.strerror}.")
    # Bytes that aren't valid UTF-8 text: the file is damaged
    except UnicodeDecodeError:
        raise ScoreError(f"{SCORES_FILE_NAME} is corrupt: it is not a text file.")
    # Editors and echo add a newline at the end, and spaces around the number are harmless
    text = text.strip()
    # Only the digits 0-9: rejects empty, text, decimals, any sign (so negatives), extra lines, non-ASCII digits
    if not (text.isascii() and text.isdigit()):
        raise ScoreError(f"{SCORES_FILE_NAME} is corrupt: expected one whole number of 0 or more.")
    return int(text)


# Save the score safely; raise ScoreError if it can't be saved. Internal: only add_score writes
def _write_score(score):
    # Write a copy first, then swap it in: a crash while writing can't empty the real file
    temp_file_path = SCORES_FILE_PATH + ".tmp"
    try:
        with open(temp_file_path, "w", encoding="utf-8") as file:
            file.write(f"{score}\n")
        # One atomic step: anyone reading sees the old total or the new one, never half a file
        os.replace(temp_file_path, SCORES_FILE_PATH)
    # No permission, a full disk: the real file still holds the old total, so nothing is lost
    except OSError as error:
        # Don't leave a half-written copy behind; it may not exist if open() itself failed
        try:
            os.remove(temp_file_path)
        except OSError:
            pass
        raise ScoreError(f"Could not save {SCORES_FILE_NAME}: {error.strerror}.")


# Add a win's points to the saved total; return the new total, or BAD_RETURN_CODE if it can't be read or saved
def add_score(difficulty):
    # The brief's formula: difficulty 1-5 earns 8, 11, 14, 17 or 20 points
    points_of_winning = (difficulty * 3) + 5
    try:
        current_score = read_score()
        new_score = current_score + points_of_winning
        _write_score(new_score)
    # A broken file or a failed save: tell the player, and never report a fake success
    except ScoreError as error:
        print(error)
        return BAD_RETURN_CODE
    return new_score
