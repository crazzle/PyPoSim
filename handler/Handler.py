import json
import logging

from concurrent.futures import ThreadPoolExecutor
from tornado import gen, web
from tornado.concurrent import run_on_executor

from actor import PlantRegistry
from plant.exception import PlantNotFoundException
from plantstorage import PlantStorage


class BaseRequestHandler(web.RequestHandler):
    logger = logging.getLogger("tornado.application")
    MAX_WORKERS = 2
    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    storage = PlantStorage.PlantStorage()
    registry = PlantRegistry

    def not_found(self, uid, msg):
        self.set_status(404)
        message = {
            'status': 404,
            'uid': uid,
            'message': msg
        }
        resp = json.dumps(message)
        return resp

    def bad_request(self, msg):
        self.set_status(400)
        message = {
            'status': 400,
            'message': 'Invalid request - ' + str(msg)
        }
        resp = json.dumps(message)
        return resp


class AllPlants(BaseRequestHandler):

    @gen.coroutine
    def get(self):
        plants = yield self.get_plants()
        raise gen.Return(self.render('../templates/show_plants.html', title="PyPoSim", plants=plants))

    @run_on_executor
    def get_plants(self):
        plants = self.storage.get_all_plants()
        return plants


class MasterData(BaseRequestHandler):

    @gen.coroutine
    def get(self, uid):
        try:
            wanted = yield self.get_master_data(uid)
            self.write(str(wanted))
        except PlantNotFoundException.PlantNotFoundException as e:
            self.write(self.not_found(e.uid, e.msg))

    @run_on_executor
    def get_master_data(self, uid):
        wanted = self.storage.get_plant_by_uid(uid)
        return wanted


class Stats(BaseRequestHandler):

    @gen.coroutine
    def get(self, uid):
        try:
            point = yield self.get_point(uid)
            self.write(str(point))
        except PlantNotFoundException.PlantNotFoundException as e:
            self.write(self.not_found(e.uid, e.msg))

    @run_on_executor
    def get_point(self, uid):
        point = self.registry.find_active_plant(uid).ask({'msg': 'stats'}, block=True, timeout=None)
        return point


class Dispatch(BaseRequestHandler):

    @gen.coroutine
    def get(self, uid, point):
        try:
            self.registry.find_active_plant(uid).tell({'msg': 'dispatch', 'value': int(point)})
            self.write(str(point))
        except PlantNotFoundException.PlantNotFoundException as e:
            self.write(self.not_found(e.uid, e.msg))
        except ValueError as ve:
            return self.bad_request(ve.message)


class Add(BaseRequestHandler):

    def validate_request(self, body):
        for k in body:
            if not body[k]:
                raise ValueError(str(k))

    @gen.coroutine
    def post(self):
        try:
            self.logger.info("add plant")
            raw = self.request.body
            self.logger.info(self.request.body)
            body = json.loads(raw)
            self.validate_request(body)
            name = body['name']
            setpoint = int(body['initial_setpoint'])
            fluctuation = int(body['fluctuation'])
            ramp = abs(int(body['ramp']))  # Because negative ramps make absolutely no sense!
            uid = yield self.persist(name, setpoint, fluctuation, ramp)
            self.write(str(uid))
        except KeyError as ke:
            self.write(self.bad_request(ke.message))
        except ValueError as ve:
            self.write(self.bad_request(ve.message))

    @run_on_executor
    def persist(self, name, setpoint, fluctuation, ramp):
        uid = self.registry.add_new_plant(name, setpoint, fluctuation, ramp)
        return uid


class Delete(BaseRequestHandler):

    @gen.coroutine
    def get(self, uid):
        try:
            yield self.destroy(uid)
            self.write("killed")
        except PlantNotFoundException.PlantNotFoundException as e:
            self.write(self.not_found(e.uid, e.msg))

    @run_on_executor
    def destroy(self, uid):
        self.registry.delete_plant(uid)




