from flask import Flask
from flask import request
from actor import SimplePlantActor
from plantstorage import PlantStorage
from pykka import ActorRegistry
import json
import time
import threading


plants = {}
storage = PlantStorage.PlantStorage()
storage.initialize_db()
for plant in storage.get_all_plants():
    plants[plant.uid] = SimplePlantActor.SimplePlantActor.start(
            plant.power,
            plant.fluctuationInPercentage,
            plant.rampInSeconds)

app = Flask(__name__)


@app.route('/masterdata/<uid>')
def get_masterdata_for_plant(uid):
    wanted = storage.get_plant_by_uid(uid)
    return str(wanted)


@app.route('/<uid>')
def get_output_for_plant(uid):
    point = plants[uid].ask({'msg': 'stats'})
    return str(point)


@app.route('/dispatch/<uid>/<point>')
def set_power_target_for_plant(uid, point):
    plants[uid].tell({'msg': 'dispatch', 'value': point})
    return str(point)


@app.route('/add', methods=['POST'])
def add_new_plant():
    raw = request.data
    body = json.loads(raw)
    uid = storage.persist(body['name'], body['power'], body['fluctuation'], body['ramp'])
    plants[uid] = SimplePlantActor.SimplePlantActor.start(body['power'], body['fluctuation'], body['ramp'])
    return str(uid)


@app.route('/delete/<uid>')
def delete_plant(uid):
    storage.destroy(uid)
    plants[uid].stop()
    del(plants[uid])
    return "killed"


def tell_tick():
    ActorRegistry.broadcast({'msg': 'tick'})


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
