from flask import Flask
from actor import SimplePlantActor


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


if __name__ == '__main__':
    app.debug = True
    app.run()
