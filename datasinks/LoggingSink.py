from streams.Streams import globalStream as stream
import json
import logging

logger = logging.getLogger(__name__)


def subscribe():
    stream.subscribe(lambda x: logger.info(json.dumps(x)))
