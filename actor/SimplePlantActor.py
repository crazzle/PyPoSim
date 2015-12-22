from plant import SimplePlant
import time, sched, pykka


class SimplePlantActor(pykka.ThreadingActor):

    def __init__(self):
        super(SimplePlantActor, self).__init__()
        self.plant = SimplePlant.SimplePlant(100, 15, 5)
        self.now = time.time()
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.schedule_tick()

    def on_receive(self, message):
        if message["msg"] == "start":
            self.actor_ref.tell({'msg': 'tick'})

        elif message["msg"] == "tick":
            self.plant = self.plant.evolve()
            self.schedule_tick()

        elif message["msg"] == "dispatch":
            self.plant = self.plant.dispatch(int(message["value"]))

        elif message["msg"] == "stats":
            return self.plant.output

    def schedule_tick(self):
        self.scheduler.enter(1, 1, self.actor_ref.tell, ({'msg': 'tick'},))
        self.scheduler.run()
