import json


class DataPoint:

    def __init__(self, id, timestamp, metric, value):
        self.id = id
        self.timestamp = timestamp
        self.metric = metric
        self.value = value

    def __repr__(self):
        dp_json = {
            "id": self.id,
            "timestamp": self.timestamp,
            "metric": self.metric,
            "value": self.value
        }
        return json.dumps(dp_json)

    def __str__(self):
        return self.__repr__()
