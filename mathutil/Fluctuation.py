import random


class Fluctuation:

    def __init__(self, percentage):
        self.percentage = percentage

    def __call__(self, value):
        return self.apply(value)

    def apply(self, value):
        return value + self.generate(value)

    def generate(self, value):
        relative_value = self.get_relative_value(value)
        corridor = (-relative_value, relative_value)
        return random.randint(corridor[0], corridor[1])

    def get_relative_value(self, value):
        relative_value = float(value)/100.0*float(self.percentage)
        return int(relative_value)
