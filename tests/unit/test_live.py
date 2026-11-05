# Unit tests for Live.py

import pytest

from Live import get_number


# monkeypatch is a pytest feature (fixture) that lets us replace functions with fake ones, for testing.
# Each row: the prompt, the range, the player's answer, and the number expected back
@pytest.mark.parametrize(
    "prompt, low, high, answer, expected",
    [
        ("Enter game number (1-3): ", 1, 3, "1", 1),
        ("Enter game number (1-3): ", 1, 3, "2", 2),
        ("Enter game number (1-3): ", 1, 3, "3", 3),
        ("Please choose game difficulty from 1 to 5: ", 1, 5, "1", 1),
        ("Please choose game difficulty from 1 to 5: ", 1, 5, "2", 2),
        ("Please choose game difficulty from 1 to 5: ", 1, 5, "3", 3),
        ("Please choose game difficulty from 1 to 5: ", 1, 5, "4", 4),
        ("Please choose game difficulty from 1 to 5: ", 1, 5, "5", 5),
        ("Enter game number (1-3): ", 1, 3, " 2 ", 2),
    ],
    ids=[
        "game 1", "game 2", "game 3",
        "difficulty 1", "difficulty 2", "difficulty 3", "difficulty 4", "difficulty 5",
        "spaces around number",
    ],
)
def test_get_number_valid_answer_is_accepted(monkeypatch, prompt, low, high, answer, expected):
    # The player's answers, in order: just one valid answer
    answers = iter([answer])
    # The player answers once, with a valid value
    monkeypatch.setattr("builtins.input", lambda text: next(answers))
    # Act: call the function with this row's prompt and range
    result = get_number(prompt, low, high)
    # Assert: the answer is accepted on the first try and returned
    assert result == expected
    # Assert: it is an int, so load_game can compare it with 1, 2 and 3
    assert isinstance(result, int)


# capsys is a pytest feature (fixture) that lets us capture what the function printed, for testing.
# it is possible to use several fixtures tools in the same test function, as long as they are listed in the parameters, separated by commas.
# One run per answer that is not a whole number
# Here we testing different type of error message
@pytest.mark.parametrize("bad_answer", ["abc", "2.5", "", " "], ids=["text", "decimal", "empty", "space"])
def test_get_number_not_whole_number_asks_again(monkeypatch, capsys, bad_answer):
    # The player's answers, in order: one that is not a whole number, then a valid number
    answers = iter([bad_answer, "2"])
    # Each input() call takes the next answer from the list
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    # Act: the function rejects the bad answer, asks again, then accepts "2"
    result = get_number("Enter game number (1-3): ", 1, 3)
    # Assert: the second answer was returned
    assert result == 2
    # Read everything the function printed
    captured = capsys.readouterr()
    # Assert: the message quotes this run's bad answer (print adds the \n)
    assert captured.out == f"'{bad_answer}' is not a whole number, please try again.\n"


# One run per answer just outside the 1-3 range
# bad_answer is the parameter name, the list of values is the second argument, and the ids are just for human-readable test names.
# then bad_answer injected to the test function as a parameter, and the test runs once for each value.
@pytest.mark.parametrize("bad_answer", ["0", "4", "-1"], ids=["below range", "above range", "negative"])
def test_get_number_out_of_range_asks_again(monkeypatch, capsys, bad_answer):
    # The player's answers, in order: one outside the range, then a valid number
    answers = iter([bad_answer, "2"])
    # Each input() call takes the next answer from the list
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    # Act: the function rejects the bad answer, asks again, then accepts "2"
    result = get_number("Enter game number (1-3): ", 1, 3)
    # Assert: the second answer was returned
    assert result == 2
    # Read everything the function printed
    captured = capsys.readouterr()
    # Assert: exactly the range message was printed (print adds the \n)
    assert captured.out == "Please choose a number from 1 to 3.\n"


