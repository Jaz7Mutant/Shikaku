from math import sqrt


class Block:
    """
    Number that should be transformed into rectangle with same area

    row, col -- position on board
    factors -- factors list of number value
    """

    def __init__(self, row: int, col: int, value: int):
        self.row = row
        self.col = col
        self.value = value
        self.factors = self._calculate_factors()
        self.factor_pointer = 0

    def _calculate_factors(self):
        """Update the factors list"""
        factors = []
        bound = round(sqrt(self.value)) + 1
        for i in range(1, int(bound)):
            if self.value % i == 0:
                if i == self.value // i:
                    factors.append(i)
                else:
                    factors.append(i)
                    factors.append(self.value // i)
        return factors
