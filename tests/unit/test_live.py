# Unit tests for Live.py

from Live import get_number


# monkeypatch is a pytest feature (fixture) that lets us replace functions with fake ones, for testing.
def test_get_number_valid_answer_returns_number(monkeypatch):
    # Arrange: the fake input answers "2", as if the player typed 2
    monkeypatch.setattr("builtins.input", lambda prompt: "2")
    # Act: call the real function with the game menu's range
    result = get_number("Enter game number (1-3): ", 1, 3)
    # Assert: it returns the number 2, as an int and not the text "2"
    assert result == 2
    assert isinstance(result, int)


# capsys is a pytest feature (fixture) that lets us capture what the function printed, for testing.
# it is possible to use several fixtures tools in the same test function, as long as they are listed in the parameters, separated by commas.
def test_get_number_text_answer_asks_again(monkeypatch, capsys):
    # The player's answers, in order: first text, then a valid number
    answers = iter(["abc", "2"])
    # Each input() call takes the next answer from the list
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    # Act: the function rejects "abc", asks again, then accepts "2"
    result = get_number("Enter game number (1-3): ", 1, 3)
    # Assert: the second answer was returned
    assert result == 2
    # Read everything the function printed during the test
    captured = capsys.readouterr()
    # Assert: exactly this message was printed, and nothing else
    # The \n at the end is the newline print() adds.
    assert captured.out == "'abc' is not a whole number, please try again.\n"