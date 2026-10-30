# Unit tests for CurrencyRouletteGame.py

from decimal import Decimal

import pytest

from CurrencyRouletteGame import get_money_interval


def test_get_money_interval_returns_decimal():
    # Act: any normal case will do; this test checks the type, not the values
    lower, upper = get_money_interval(10, 3.60, 2)
    # Assert: money stays exact, so both edges are Decimal, never float
    assert isinstance(lower, Decimal)
    assert isinstance(upper, Decimal)

# Each row: USD amount, rate, difficulty, then the expected lower and upper edges
@pytest.mark.parametrize(
    "usd_amount, rate, difficulty, expected_lower, expected_upper",
    [
        (10, 3.60, 1, Decimal("32.00"), Decimal("40.00")),
        (10, 3.60, 2, Decimal("33.00"), Decimal("39.00")),
        (10, 3.60, 3, Decimal("34.00"), Decimal("38.00")),
        (10, 3.60, 4, Decimal("35.00"), Decimal("37.00")),
        (10, 3.60, 5, Decimal("36.00"), Decimal("36.00")),
        (7, 3.109125, 3, Decimal("19.76"), Decimal("23.76")),
        (1, 3.105, 5, Decimal("3.11"), Decimal("3.11")),
    ],
    ids=["margin 4", "margin 3", "margin 2", "margin 1", "margin 0", "real rate rounded", "half rounds up"],
)
def test_get_money_interval_edges(usd_amount, rate, difficulty, expected_lower, expected_upper):
    # Act: unpack the two edges the function returns
    lower, upper = get_money_interval(usd_amount, rate, difficulty)
    # Assert: both edges match the hand-calculated values
    assert lower == expected_lower
    assert upper == expected_upper