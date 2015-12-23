from plant import SimplePlant
import pykka


class SimplePlantActor(pykka.ThreadingActor):

    def __init__(self):
        super(SimplePlantActor, self).__init__()
        self.plant = SimplePlant.SimplePlant(100, 15, 5)

    def on_receive(self, message):
        if message["msg"] == "tick":
            self.plant = self.plant.evolve()

        elif message["msg"] == "dispatch":
            self.plant = self.plant.dispatch(int(message["value"]))

        elif message["msg"] == "stats":
            return self.plant.output
