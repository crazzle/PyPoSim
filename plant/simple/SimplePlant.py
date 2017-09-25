import copy
import datetime

from Ramp import Ramp
from datasinks.Streams import globalStream as stream
from plant.data import DataPoint
from plant.simple import Fluctuation


class SimplePlant:

    def __init__(self, plant_id, capacity, fluctuation_in_percent, ramp_per_second):
        self.plant_id = plant_id
        self.capacity = capacity
        self.setpoint = capacity
        self.output = capacity
        self.percentage = fluctuation_in_percent
        self.fluctuation = Fluctuation.Fluctuation(fluctuation_in_percent, capacity)
        self.rampPerSecond = ramp_per_second
        self.ramp = Ramp(capacity, capacity, ramp_per_second)

    def evolve(self):
        state = copy.deepcopy(self)
        new_ramp = self.ramp.evolve()
        state.ramp = new_ramp
        state.setpoint = new_ramp.power
        state.output = self.fluctuation(state.setpoint)
        state.output = state.output if state.output > 0 else 0
        state.emit_all()
        return state

    def dispatch(self, setpoint):
        state = copy.deepcopy(self)
        if setpoint < 0:
            setpoint = 0
        elif setpoint > self.capacity:
            setpoint = self.capacity
        state.ramp = self.ramp.start(setpoint, self.setpoint)
        state.emit("dispatch", setpoint)
        return state

    def emit_all(self):
        self.emit("setpoint", self.setpoint)
        self.emit("power_output", self.output)

    def emit(self, metric, value):
        dp = DataPoint.DataPoint(self.plant_id, datetime.datetime.now().isoformat(), metric, value)
        stream.on_next(dp)
