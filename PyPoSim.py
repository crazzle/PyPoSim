from flask import Flask
from flask import request
from actor import SimplePlantActor
from plantstorage import PlantStorage
from pykka import ActorRegistry
from plantexception import PlantNotFoundException
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


@app.route('/')
def get_all_plants():
    return json.dumps([p.__dict__ for p in storage.get_all_plants()])


@app.route('/masterdata/<uid>')
def get_masterdata_for_plant(uid):
    try:
        wanted = storage.get_plant_by_uid(uid)
        return str(wanted)
    except PlantNotFoundException.PlantNotFoundException as e:
        return not_found(e.uid, e.msg)


@app.route('/<uid>')
def get_output_for_plant(uid):
    try:
        point = find_active_plant(uid).ask({'msg': 'stats'})
        return str(point)
    except PlantNotFoundException.PlantNotFoundException as e:
        return not_found(e.uid, e.msg)


@app.route('/dispatch/<uid>/<point>')
def set_power_target_for_plant(uid, point):
    try:
        find_active_plant(uid).tell({'msg': 'dispatch', 'value': point})
        return str(point)
    except PlantNotFoundException.PlantNotFoundException as e:
        return not_found(e.uid, e.msg)


@app.route('/add', methods=['POST'])
def add_new_plant():
    try:
        raw = request.data
        body = json.loads(raw)
        uid = storage.persist(body['name'], body['power'], body['fluctuation'], body['ramp'])
        plants[uid] = SimplePlantActor.SimplePlantActor.start(body['power'], body['fluctuation'], body['ramp'])
        return str(uid)
    except KeyError:
        return not_created()


@app.route('/delete/<uid>')
def delete_plant(uid):
    try:
        storage.destroy(uid)
        find_active_plant(uid).stop()
        del(plants[uid])
        return "killed"
    except PlantNotFoundException.PlantNotFoundException as e:
        return not_found(e.uid, e.msg)


def find_active_plant(uid):
    try:
        return plants[uid]
    except KeyError:
        raise PlantNotFoundException.PlantNotFoundException("Plant not found in running plants", uid)


def not_found(uid, msg):
    message = {
            'status': 404,
            'uid': uid,
            'message': msg
    }
    resp = json.dumps(message)
    return resp, 404


def not_created():
    message = {
            'status': 400,
            'message': 'Invalid request'
    }
    resp = json.dumps(message)
    return resp, 400


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
