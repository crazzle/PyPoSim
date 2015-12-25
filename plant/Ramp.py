import copy
import time


class Ramp:

    def __init__(self, target, power, ramp_per_second):
        self.power = power
        self.target = target
        self.now = time.time()
        self.rampPerSecond = ramp_per_second

    def evolve(self):
        new_state = copy.deepcopy(self)
        now = time.time()
        diff = now - self.now
        new_state.now = now
        if diff >= 1:
            if self.is_ramp_at_end(self.power, self.target):
                new_state.power = self.target
            elif self.power < self.target:
                new_state.power = self.power + self.rampPerSecond
            elif self.power > self.target:
                new_state.power = self.power - self.rampPerSecond
        return new_state

    def start(self, target, power):
        new_state = copy.deepcopy(self)
        now = time.time()
        new_state.now = now
        new_state.target = target
        new_state.power = power
        return new_state

    def is_ramp_at_end(self, current_power, target):
        result = abs(current_power-target) <= self.rampPerSecond
        return result
