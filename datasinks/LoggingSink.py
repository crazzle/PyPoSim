from streams.Streams import globalStream as stream
import json
import logging
import util.Config as Config


logger = logging.getLogger(__name__)
fh = logging.FileHandler(Config.get_history_config()["filename"])
fh.setLevel(logging.INFO)
logger.addHandler(fh)


def subscribe():
    stream.subscribe(lambda x: logger.info(json.dumps(x)))
