import random


class Fluctuation:

    def __init__(self, percentage, baseline):
        self.percentage = percentage
        self.baseline = baseline

    def __call__(self, value):
        return self.apply(value)

    def apply(self, value):
        return value + self.generate(self.baseline)

    def generate(self, baseline):
        relative_value = self.get_relative_value(baseline)
        corridor = (-relative_value, relative_value)
        return random.randint(corridor[0], corridor[1])

    def get_relative_value(self, baseline):
        relative_value = float(baseline) / 100.0 * float(self.percentage)
        return int(relative_value)
