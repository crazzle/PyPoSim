from streams.Streams import globalStream as stream
import logging
import util.Config as Config


logger = logging.getLogger(__name__)
fh = logging.FileHandler(Config.get_history_config()["filename"])
fh.setLevel(logging.INFO)
logger.addHandler(fh)


def subscribe():
    stream.subscribe(lambda dp: logger.info(dpToCSV(dp)))


def dpToCSV(dp):
    ts = str(dp.timestamp)
    metric = str(dp.metric)
    dp_id = str(dp.id)
    value = str(dp.value)
    csv = ts + ";" + metric + ";" + dp_id + ";" + value
    return csv