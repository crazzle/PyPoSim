from plant import SimplePlant
import pykka


class SimplePlantActor(pykka.ThreadingActor):

    def __init__(self, plant_id, internal_setpoint, fluctuation, ramp):
        super(SimplePlantActor, self).__init__()
        self.plant_id = plant_id
        self.plant = SimplePlant.SimplePlant(plant_id, internal_setpoint, fluctuation, ramp)

    def on_receive(self, message):
        if message["msg"] == "tick":
            self.plant = self.plant.evolve()

        elif message["msg"] == "dispatch":
            self.plant = self.plant.dispatch(int(message["value"]))

        elif message["msg"] == "stats":
            return self.plant.output
