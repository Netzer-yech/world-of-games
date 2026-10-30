# Unit tests for MemoryGame.py

import pytest

from MemoryGame import generate_sequence, is_list_equal


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