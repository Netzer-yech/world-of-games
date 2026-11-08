# Unit tests for MemoryGame.py

import pytest

from MemoryGame import generate_sequence, get_list_from_user, is_list_equal


def test_is_list_equal_same_lists_returns_true():
    # Same numbers in the same order: the player repeated the sequence correctly
    assert is_list_equal([5, 42, 101], [5, 42, 101]) is True


# Each tuple is one case: (the sequence shown, what the player typed)
@pytest.mark.parametrize(
    "sequence, user_list",
    [
        ([5, 42, 101], [5, 42, 100]),
        ([5, 42, 101], [42, 5, 101]),
        ([5, 42, 101], [5, 42]),
        ([5, 42, 101], [5, 42, 101, 7]),
    ],
    # A readable name for each case, shown in the report
    ids=["wrong number", "wrong order", "missing number", "extra number"],
)
def test_is_list_equal_different_lists_returns_false(sequence, user_list):
    # Any difference means the player did not repeat the sequence correctly
    assert is_list_equal(sequence, user_list) is False


# Run once for each difficulty
@pytest.mark.parametrize("difficulty", [1, 2, 3, 4, 5])
def test_generate_sequence_matches_difficulty(difficulty):
    # Act: build a sequence for this difficulty
    sequence = generate_sequence(difficulty)
    # It is a list, so it can be compared with the player's list
    assert isinstance(sequence, list)
    # It has exactly as many numbers as the difficulty
    assert len(sequence) == difficulty
    # Check every number in the sequence, one by one
    for number in sequence:
        # A whole number, from 1 to 101 inclusive
        assert isinstance(number, int)
        assert 1 <= number <= 101


# Each row: the difficulty, what the player types, and the list expected back
@pytest.mark.parametrize(
    "difficulty, answer, expected",
    [
        (1, "5", [5]),
        (2, "5 42", [5, 42]),
        (3, "5 42 101", [5, 42, 101]),
        (4, "1 2 3 4", [1, 2, 3, 4]),
        (5, "101 1 50 7 7", [101, 1, 50, 7, 7]),
        (3, "  5   42 101  ", [5, 42, 101]),
    ],
    ids=["difficulty 1", "difficulty 2", "difficulty 3", "difficulty 4", "difficulty 5", "extra spaces"],
)
def test_get_list_from_user_valid_answer_is_accepted(monkeypatch, difficulty, answer, expected):
    # The player's only answer: a valid sequence
    answers = iter([answer])
    # An empty list that will record every prompt the game shows
    prompts = []

    # A fake input(): it records the prompt, then returns the next answer
    def fake_input(text):
        prompts.append(text)
        return next(answers)

    # Replace the real input() with the fake one, for this test only
    monkeypatch.setattr("builtins.input", fake_input)
    # Act: ask for the sequence at this row's difficulty
    result = get_list_from_user(difficulty)
    # Assert: the numbers come back as a list of ints, in the typed order
    assert result == expected
    assert isinstance(result, list)
    # Assert: the game asked exactly once, naming how many numbers to enter
    assert prompts == [f"Enter the {difficulty} numbers you saw, separated by spaces: "]