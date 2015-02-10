from __future__ import unicode_literals


class Cashier(object):
    """Greedy coin change problem solver.

    """

    def __init__(self, denominations):
        self.denominations = denominations

    def __call__(self, value):
        result = {}
        remain = value
        for denomination in reversed(self.denominations):
            if not remain:
                break
            coin_count = remain / denomination
            if not coin_count:
                continue
            result[denomination] = coin_count
            remain = remain % denomination
        return result
