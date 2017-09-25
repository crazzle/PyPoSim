import logging
from tornado import ioloop, web
from pykka import ActorRegistry
from actor import PlantRegistry
from handler import Handler
import util.Config as Config
import datasinks.LoggingSink as LoggingSink
import datasinks.KafkaSink as KafkaSink

def tell_tick():
    ActorRegistry.broadcast({'msg': 'tick'})

if __name__ == '__main__':
    ## configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("tornado.application")
    logger.info("starting application PyPoSim...")

    ## adding standard plant
    if Config.get_startup_config()["add_default_plant"]:
        PlantRegistry.add_new_plant("Default", 100, 10, 5)

    ## register datasinks
    if Config.get_kafka_config()["enabled"]:
        KafkaSink.subscribe()
    if Config.get_history_config()["enabled"]:
        logger.info("history enabled")
        LoggingSink.subscribe()

    app = web.Application([("/", Handler.AllPlants),
                           ("/add", Handler.Add),
                           (r"/([a-zA-Z0-9]{2,})", Handler.Stats),
                           (r"/masterdata/([a-zA-Z0-9]{2,})", Handler.MasterData),
                           (r"/dispatch/([a-zA-Z0-9]{2,})/(\d+)", Handler.Dispatch),
                           (r"/delete/([a-zA-Z0-9]{2,})", Handler.Delete)])
    app.listen(5000)
    loop = ioloop.IOLoop.current()
    ioloop.PeriodicCallback(tell_tick,1000).start()
    loop.start()

