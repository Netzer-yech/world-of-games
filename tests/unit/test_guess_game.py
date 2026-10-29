# Unit tests for GuessGame.py

import pytest

from GuessGame import compare_results, generate_number


def test_compare_results_same_number_return_true():
    # the guess match to the secret number, player wins
    assert compare_results(3, 3) is True


def test_compare_results_different_number_returns_false():
    # The guess is wrong, so the player loses, validate that function return also False
    assert compare_results(3, 4) is False