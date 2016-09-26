from plant import SimplePlant
import pykka
from streams.Streams import globalStream as stream
import datetime


class SimplePlantActor(pykka.ThreadingActor):

    def __init__(self, id, power, fluctuation, ramp):
        super(SimplePlantActor, self).__init__()
        self.id = id
        self.plant = SimplePlant.SimplePlant(power, fluctuation, ramp)

    def on_receive(self, message):
        if message["msg"] == "tick":
            self.plant = self.plant.evolve()
            stream.on_next({
                "id": self.id,
                "timestamp": datetime.datetime.now().isoformat(),
                "metric": "active_power",
                "value": self.plant.output
            })

        elif message["msg"] == "dispatch":
            self.plant = self.plant.dispatch(int(message["value"]))

        elif message["msg"] == "stats":
            return self.plant.output
