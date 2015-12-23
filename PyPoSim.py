from flask import Flask
from actor import SimplePlantActor
import time, threading


ref = SimplePlantActor.SimplePlantActor.start()
app = Flask(__name__)

@app.route('/')
def get_power_for_plant():
    power = ref.ask({'msg': 'stats'})
    return str(power)


@app.route('/dispatch/<point>')
def set_power_target_for_plant(point):
    ref.tell({'msg': 'dispatch', 'value': point})
    return str(point)


def tell_tick():
    ref.tell({'msg': 'tick'})


def schedule_tick():
    tell_tick()
    time.sleep(1)
    run_async_tick()


def run_async_tick():
    threading.Thread(target=schedule_tick).start()

run_async_tick()

if __name__ == '__main__':
    app.debug = True
    app.run()
