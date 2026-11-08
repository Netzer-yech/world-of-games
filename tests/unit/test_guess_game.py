# Unit tests for GuessGame.py

import pytest

from GuessGame import compare_results, generate_number, get_guess_from_user


def test_compare_results_same_number_returns_true():
    # the guess match to the secret number, player wins
    assert compare_results(3, 3) is True


def test_compare_results_different_number_returns_false():
    # The guess is wrong, so the player loses, validate that function return also False
    assert compare_results(3, 4) is False


# Run this test 5 times, once for each difficulty value in the list
@pytest.mark.parametrize("difficulty", [1, 2, 3, 4, 5])
# pytest passes each value from the list into this parameter
def test_generate_number_is_within_range(difficulty):
    # Act: call the real function with this run's difficulty
    number = generate_number(difficulty)
    # Assert: the secret number is between 1 and difficulty, inclusive
    assert 1 <= number <= difficulty
    # Assert: it is a whole number, so it can match the player's guess
    assert isinstance(number, int)


# Each row: the difficulty, the player's guess, and the number expected back
@pytest.mark.parametrize(
    "difficulty, answer, expected",
    [
        (1, "1", 1),
        (2, "1", 1),
        (2, "2", 2),
        (3, "1", 1),
        (3, "3", 3),
        (4, "1", 1),
        (4, "4", 4),
        (5, "1", 1),
        (5, "5", 5),
        (3, " 2 ", 2),
    ],
    ids=[
        "difficulty 1 only value",
        "difficulty 2 lowest", "difficulty 2 highest",
        "difficulty 3 lowest", "difficulty 3 highest",
        "difficulty 4 lowest", "difficulty 4 highest",
        "difficulty 5 lowest", "difficulty 5 highest",
        "spaces around guess",
    ],
)
def test_get_guess_from_user_valid_guess_is_accepted(monkeypatch, difficulty, answer, expected):
    # The player's only answer: a valid guess
    answers = iter([answer])
    # An empty list that will record every prompt the game shows
    prompts = []

    # A fake input(): it records the prompt for later inspection, then returns the next answer
    # The text is the prompt the game passed to input(), and the return value is what the player typed
    def fake_input(text):
        # Save the prompt text the game passed to input()
        prompts.append(text)
        # Answer like a player would
        return next(answers)

    # Using fake_input name to run the function instead of the real input() function, only for this test
    monkeypatch.setattr("builtins.input", fake_input)
    # Act: ask for a guess at this row's difficulty
    result = get_guess_from_user(difficulty)
    # Assert: the guess is accepted on the first try and returned as an int
    assert result == expected
    assert isinstance(result, int)
    # Assert: the game asked exactly once, with the range of this difficulty
    assert prompts == [f"Guess a number from 1 to {difficulty}: "]


# One run per guess that is not a whole number
@pytest.mark.parametrize("bad_answer", ["abc", "2.5", "", " "], ids=["text", "decimal", "empty", "space"])
def test_get_guess_from_user_not_whole_number_asks_again(monkeypatch, capsys, bad_answer):
    # The player's answers, in order: one that is not a whole number, then a valid guess
    answers = iter([bad_answer, "2"])
      # Each input() call takes the next answer from the list
      # lambda is a nameless one-line function that ignores the prompt and returns the next answer
    monkeypatch.setattr("builtins.input", lambda text: next(answers))
    # Act: the game rejects the bad answer, asks again, then accepts "2"
    result = get_guess_from_user(3)
    # Assert: the second answer was returned
    assert result == 2
    # Read everything the game printed
    captured = capsys.readouterr()
    # Assert: the message quotes this run's bad answer (print adds the \n)
    assert captured.out == f"'{bad_answer}' is not a whole number, please try again.\n"


# Each row: the difficulty, and a guess just outside its range
@pytest.mark.parametrize(
    "difficulty, bad_answer",
    [
        (1, "0"), (1, "2"),
        (2, "0"), (2, "3"),
        (3, "0"), (3, "4"),
        (4, "0"), (4, "5"),
        (5, "0"), (5, "6"),
    ],
    ids=[
        "difficulty 1 below", "difficulty 1 above",
        "difficulty 2 below", "difficulty 2 above",
        "difficulty 3 below", "difficulty 3 above",
        "difficulty 4 below", "difficulty 4 above",
        "difficulty 5 below", "difficulty 5 above",
    ],
)
def test_get_guess_from_user_out_of_range_asks_again(monkeypatch, capsys, difficulty, bad_answer):
    # The player's answers, in order: one outside the range, then "1", valid at every difficulty
    answers = iter([bad_answer, "1"])
    # Each input() call takes the next answer from the list
    # lambda is a nameless one-line function that ignores the prompt and returns the next answer
    monkeypatch.setattr("builtins.input", lambda text: next(answers))
    # Act: the game rejects the bad guess, asks again, then accepts "1"
    result = get_guess_from_user(difficulty)
    # Assert: the second answer was returned
    assert result == 1
    # Read everything the game printed
    captured = capsys.readouterr()
    # Assert: the message names this difficulty's range (print adds the \n)
    assert captured.out == f"Please choose a number from 1 to {difficulty}.\n"