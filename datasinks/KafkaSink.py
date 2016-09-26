from kafka import KafkaProducer
from streams.Streams import globalStream as stream
import json
import util.Config as Config
import logging

logger = logging.getLogger(__name__)
kafka_config = Config.get_kafka_config()

server = kafka_config["server"]
port = kafka_config["port"]
topic = kafka_config["topic"]
producer = KafkaProducer(bootstrap_servers=server+":"+port)


def subscribe():
    logger.info("subscribing for kafka sink")
    stream.subscribe(lambda x: producer.send(topic, json.dumps(x)))

