from kafka import KafkaProducer
from streams.Streams import globalStream as stream
import json
import util.Config as Config
import logging
from concurrent import futures


# on top for pickling
def subscribe_async():
    try:
        producer = KafkaProducer(bootstrap_servers=server + ":" + port)
        stream.subscribe(lambda x: producer.send(topic, json.dumps(x)))
    except Exception as e:
        logger.error("could not connect to kafka broker because of " + str(e))

logger = logging.getLogger(__name__)
kafka_config = Config.get_kafka_config()

server = kafka_config["server"]
port = kafka_config["port"]
topic = kafka_config["topic"]


# Subscribe has to be non-blocking in case of wrong configuration
def subscribe():
    logger.info("subscribing for kafka sink")
    futures.ThreadPoolExecutor(max_workers=2).submit(subscribe_async)




