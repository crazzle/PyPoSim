from streams.Streams import globalPowerStream as powerStream
import json
import logging

logger = logging.getLogger(__name__)


def subscribe():
    powerStream.subscribe(lambda x: logger.info(json.dumps(x)))
