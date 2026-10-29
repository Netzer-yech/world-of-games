# Unit tests for GuessGame.py

import pytest

from GuessGame import compare_results, generate_number


def test_compare_results_same_number_return_true():
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