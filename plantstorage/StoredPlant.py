class StoredPlant:

    def __init__(self, uid, name, capacity, fluctuation_in_percentage, ramp_in_seconds):
        self.uid = uid
        self.name = name
        self.capacity = capacity
        self.fluctuationInPercentage = fluctuation_in_percentage
        self.rampInSeconds = ramp_in_seconds

    def __repr__(self):
        plant_str = "UID: " + str(self.uid) + " "
        plant_str += "Name: " + str(self.name) + " "
        plant_str += "Capacity: " + str(self.capacity) + " "
        plant_str += "Fluctuation (%):" + str(self.fluctuationInPercentage) + " "
        plant_str += "Ramp (kw/s):" + str(self.rampInSeconds)
        return plant_str

    def __str__(self):
        plant_str = "UID: " + str(self.uid) + " "
        plant_str += "Name: " + str(self.name) + " "
        plant_str += "Capacity: " + str(self.capacity) + " "
        plant_str += "Fluctuation (%):" + str(self.fluctuationInPercentage) + " "
        plant_str += "Ramp (kw/s):" + str(self.rampInSeconds)
        return plant_str
