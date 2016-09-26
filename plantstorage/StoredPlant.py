class StoredPlant:

    def __init__(self, uid, name, power, fluctuation_in_percentage, ramp_in_seconds):
        self.uid = uid
        self.name = name
        self.power = power
        self.fluctuationInPercentage = fluctuation_in_percentage
        self.rampInSeconds = ramp_in_seconds

    def __repr__(self):
        plant_str = "UID: " + str(self.uid) + " "
        plant_str += "Name: " + str(self.name) + " "
        plant_str += "power: " + str(self.power) + " "
        plant_str += "fluctuation (%):" + str(self.fluctuationInPercentage) + " "
        plant_str += "ramp (kw/s):" + str(self.rampInSeconds)
        return plant_str

    def __str__(self):
        plant_str = "UID: " + str(self.uid) + " "
        plant_str += "Name: " + str(self.name) + " "
        plant_str += "power: " + str(self.power) + " "
        plant_str += "fluctuation (%):" + str(self.fluctuationInPercentage) + " "
        plant_str += "ramp (kw/s):" + str(self.rampInSeconds)
        return plant_str
