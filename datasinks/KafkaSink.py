from kafka import KafkaProducer
from streams.Streams import globalStream as stream
import json
import util.Config as Config


kafka_config = Config.get_kafka_config()

server = kafka_config["server"]
port = kafka_config["port"]
topic = kafka_config["topic"]
producer = KafkaProducer(bootstrap_servers=server+":"+port)


def subscribe():
    stream.subscribe(lambda x: producer.send(topic, json.dumps(x)))

