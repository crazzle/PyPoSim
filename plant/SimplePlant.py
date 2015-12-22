import copy
import time
from mathutil import Fluctuation


class SimplePlant:

    def __init__(self, power, percentage, ramp_per_second):
        self.power = power
        self.output = power
        self.percentage = percentage
        self.fluctuation = Fluctuation.Fluctuation(percentage)
        self.rampPerSecond = ramp_per_second
        self.now = time.time()
        self.ramp = lambda x: x

    def evolve_power(self):
        return self.fluctuation(self.power)

    def evolve(self):
        now = time.time()
        diff = now - self.now
        if diff >= 1:
            state = copy.deepcopy(self)
            new_power = state.ramp(state.power)
            if new_power != state.power:
                state.power = new_power
            elif new_power == self.power:
                state.ramp = lambda x: x
            state.output = state.evolve_power()
            state.now = now
            return state
        else:
            return self

    def dispatch(self, target):
        def ramp(current_power):
            if self.is_ramp_at_end(current_power, target):
                return target
            elif current_power < target:
                return current_power + self.rampPerSecond
            elif current_power > target:
                return current_power - self.rampPerSecond

        state = copy.deepcopy(self)
        state.ramp = ramp
        state.power = state.ramp(state.power)
        return state

    def is_ramp_at_end(self, current_power, target):
            result = abs(current_power-target) <= self.rampPerSecond
            return result
