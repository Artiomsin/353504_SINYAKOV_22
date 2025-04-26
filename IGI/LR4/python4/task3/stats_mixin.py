import statistics

class StatsMixin:
    def mean(self):
        return sum(self.values) / len(self.values) if len(self.values) > 0 else 0

    def median(self):
        return statistics.median(self.values) if len(self.values) > 1 else self.values[0] if self.values else 0

    def mode(self):
        try:
            return statistics.mode(self.values)
        except statistics.StatisticsError:
            return "No unique mode" if len(self.values) > 1 else self.values[0]

    def variance(self):
        return statistics.variance(self.values) if len(self.values) > 1 else "Not enough data to calculate variance"

    def standard_deviation(self):
        return statistics.stdev(self.values) if len(self.values) > 1 else "Not enough data to calculate standard deviation"
