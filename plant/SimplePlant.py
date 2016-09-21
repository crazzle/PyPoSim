import copy
from Ramp import Ramp
from mathutil import Fluctuation


class SimplePlant:

    def __init__(self, power, fluctuation_in_percent, ramp_per_second):
        self.power = power
        self.output = power
        self.percentage = fluctuation_in_percent
        self.fluctuation = Fluctuation.Fluctuation(fluctuation_in_percent, power)
        self.rampPerSecond = ramp_per_second
        self.ramp = Ramp(power, power, ramp_per_second)

    def evolve(self):
        state = copy.deepcopy(self)
        new_ramp = self.ramp.evolve()
        state.ramp = new_ramp
        state.power = new_ramp.power
        state.output = self.fluctuation(self.power)
        return state

    def dispatch(self, target):
        state = copy.deepcopy(self)
        state.ramp = self.ramp.start(target, self.power)
        return state
