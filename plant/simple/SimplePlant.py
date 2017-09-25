import copy
import datetime

from Ramp import Ramp
from datasinks.Streams import globalStream as stream
from plant.data import DataPoint
from plant.simple import Fluctuation


class SimplePlant:

    def __init__(self, plant_id, internal_setpoint, fluctuation_in_percent, ramp_per_second):
        self.plant_id = plant_id
        self.internal_setpoint = internal_setpoint
        self.output = internal_setpoint
        self.percentage = fluctuation_in_percent
        self.fluctuation = Fluctuation.Fluctuation(fluctuation_in_percent, internal_setpoint)
        self.rampPerSecond = ramp_per_second
        self.ramp = Ramp(internal_setpoint, internal_setpoint, ramp_per_second)

    def evolve(self):
        state = copy.deepcopy(self)
        new_ramp = self.ramp.evolve()
        state.ramp = new_ramp
        state.internal_setpoint = new_ramp.power
        state.output = self.fluctuation(state.internal_setpoint)
        state.emit_all()
        return state

    def dispatch(self, internal_setpoint):
        state = copy.deepcopy(self)
        state.ramp = self.ramp.start(internal_setpoint, self.internal_setpoint)
        state.emit("dispatch", internal_setpoint)
        return state

    def emit_all(self):
        self.emit("internal_setpoint", self.internal_setpoint)
        self.emit("power_output", self.output)

    def emit(self, metric, value):
        dp = DataPoint.DataPoint(self.plant_id, datetime.datetime.now().isoformat(), metric, value)
        stream.on_next(dp)
