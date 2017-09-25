import logging

import util.Config as Config
from datasinks.Streams import globalStream as stream

logger = logging.getLogger(__name__)
fh = logging.FileHandler(Config.get_history_config()["filename"], mode='w')
fh.setLevel(logging.INFO)
logger.addHandler(fh)


def subscribe():
    header = "ts;metric;plant_id;value"
    logger.info(header)
    stream.subscribe(lambda dp: logger.info(dp_to_csv(dp)))


def dp_to_csv(dp):
    ts = str(dp.timestamp)
    metric = str(dp.metric)
    plant_id = str(dp.plant_id)
    value = str(dp.value)
    csv = ts + ";" + metric + ";" + plant_id + ";" + value
    return csv
