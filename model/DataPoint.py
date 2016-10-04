import json


class DataPoint:

    def __init__(self, plant_id, timestamp, metric, value):
        self.plant_id = plant_id
        self.timestamp = timestamp
        self.metric = metric
        self.value = value

    def __repr__(self):
        dp_json = {
            "plantId": self.plant_id,
            "timestamp": self.timestamp,
            "metric": self.metric,
            "value": self.value
        }
        return json.dumps(dp_json)

    def __str__(self):
        return self.__repr__()
