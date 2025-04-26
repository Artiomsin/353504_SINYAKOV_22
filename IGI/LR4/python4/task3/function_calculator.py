import math
from abc import ABC, abstractmethod
from stats_mixin import StatsMixin

class FunctionCalculator(ABC):
    def __init__(self, x: float, eps: float):
        self.x = x
        self.eps = eps

    @abstractmethod
    def calculate_series(self) -> tuple[float, int, list]:
        pass

    @abstractmethod
    def calculate_function(self) -> float:
        pass

class ArcsinCalculator(FunctionCalculator, StatsMixin):
    def __init__(self, x: float, eps: float):
        super().__init__(x, eps)
        self.values = []

    def calculate_series(self) -> tuple[float, int, list]:
        if abs(self.x) > 1:
            raise ValueError("x must be in the range (-1, 1)")

        sum_total = self.x  # First term (n=0)
        terms_added = 1
        self.values = [sum_total]  # To track the sequence of sums
        max_terms = 500

        for n in range(1, max_terms):
            term = (math.factorial(2 * n) / ((4 ** n) * (math.factorial(n) ** 2) * (2 * n + 1))) * (self.x ** (2 * n + 1))
            if abs(term) < self.eps:
                break
            sum_total += term
            terms_added += 1
            self.values.append(sum_total)

        return sum_total, terms_added, self.values

    def calculate_function(self) -> float:
        return math.asin(self.x)
