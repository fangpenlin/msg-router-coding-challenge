from __future__ import unicode_literals

import pytest

from msg_router.models.cashier import Cashier


coin_change_data = [
    (0, {}),
    (1, {1: 1}),
    (50, {25: 2}),
    (123, {25: 4, 10: 2, 1: 3}),
    (100, {25: 4}),
    (101, {25: 4, 1: 1}),
]


@pytest.fixture
def cashier():
    """Denominations we can use for making change. Please notice that, the
    denominations we use here is for greedy coin change algorithm, not for
    dynamic programming coin change algorithm. All elements in the,
    denominations, their subset need to have only worser solutions (more coins).

    """
    return Cashier([1, 5, 10, 25])


@pytest.mark.parametrize('value,expected', coin_change_data)
def test_coin_change(cashier, value, expected):
    assert cashier(value) == expected
