from flask import Flask
from flask import render_template
from flask import request
from actor import SimplePlantActor
from plantstorage import PlantStorage
from pykka import ActorRegistry
from plantexception import PlantNotFoundException
import json
import time
import threading
import logging
import datasinks.LoggingSink as LoggingSink
import datasinks.KafkaSink as KafkaSink
import util.Config as Config

plants = {}
storage = PlantStorage.PlantStorage()
storage.initialize_db()
for plant in storage.get_all_plants():
    plants[plant.uid] = SimplePlantActor.SimplePlantActor.start(
            plant.uid,
            plant.internal_setpoint,
            plant.fluctuationInPercentage,
            plant.rampInSeconds)

app = Flask(__name__)


@app.route('/')
def get_all_plants():
    return render_template('show_plants.html', plants=storage.get_all_plants())


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
        find_active_plant(uid).tell({'msg': 'dispatch', 'value': int(point)})
        return str(point)
    except PlantNotFoundException.PlantNotFoundException as e:
        return not_found(e.uid, e.msg)
    except ValueError as ve:
        return bad_request(ve.message)


@app.route('/add', methods=['POST'])
def add_new_plant():
    try:
        raw = request.data
        body = json.loads(raw)
        validate_request(body)
        name = body['name']
        setpoint = int(body['internal_setpoint'])
        fluctuation = int(body['fluctuation'])
        ramp = abs(int(body['ramp']))  # Because negative ramps make absolutely no sense!
        uid = storage.persist(name, setpoint, fluctuation, ramp)
        plants[uid] = SimplePlantActor.SimplePlantActor.start(uid, setpoint, fluctuation, ramp)
        return str(uid)
    except KeyError as ke:
        return bad_request(ke.message)
    except ValueError as ve:
        return bad_request(ve.message)


def validate_request(body):
    for k in body:
        if not body[k]:
            raise ValueError(str(k))


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


def bad_request(msg):
    message = {
            'status': 400,
            'message': 'Invalid request - ' + str(msg)
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

if __name__ == '__main__':
    ## configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("starting application PyPoSim...")

    ## adding standard plant
    if Config.get_startup_config()["add_plants"]:
        app.logger.info("adding standard plants...")
        uid_standard_1 = storage.persist("Standard 1", 100, 10, 5)
        plants[uid_standard_1] = SimplePlantActor.SimplePlantActor.start(uid_standard_1, 100, 10, 5)
        uid_standard_2 = storage.persist("Standard 2", 500, 50, 25)
        plants[uid_standard_2] = SimplePlantActor.SimplePlantActor.start(uid_standard_2, 500, 50, 25)

    ## bootstrapping simulator
    run_async_tick()

    ## register datasinks
    if Config.get_kafka_config()["enabled"]:
        KafkaSink.subscribe()
    if Config.get_history_config()["enabled"]:
        logger.info("history enabled")
        LoggingSink.subscribe()

    ## run flask app
    app.run(host='0.0.0.0')
