import pykka

from plant.simple import SimplePlant


class SimplePlantActor(pykka.ThreadingActor):

    def __init__(self, plant_id, capacity, fluctuation, ramp):
        super(SimplePlantActor, self).__init__()
        self.plant_id = plant_id
        self.plant = SimplePlant.SimplePlant(plant_id, capacity, fluctuation, ramp)

    def on_receive(self, message):
        if message["msg"] == "tick":
            self.plant = self.plant.evolve()

        elif message["msg"] == "dispatch":
            self.plant = self.plant.dispatch(int(message["value"]))

        elif message["msg"] == "stats":
            return self.plant.output
