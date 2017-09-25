from actor import SimplePlantActor
from plant.exception import PlantNotFoundException
from plantstorage import PlantStorage

plants = {}
storage = PlantStorage.PlantStorage()
storage.initialize_db()
for plant in storage.get_all_plants():
    plants[plant.uid] = SimplePlantActor.SimplePlantActor.start(
            plant.uid,
            plant.initial_setpoint,
            plant.fluctuationInPercentage,
            plant.rampInSeconds)


def find_active_plant(uid):
    try:
        return plants[uid]
    except KeyError:
        raise PlantNotFoundException.PlantNotFoundException("Plant not found in running plants", uid)


def add_new_plant(name, setpoint, fluctuation, ramp):
    uid = storage.persist(name, setpoint, fluctuation, ramp)
    plants[uid] = SimplePlantActor.SimplePlantActor.start(uid, setpoint, fluctuation, ramp)
    return uid


def delete_plant(uid):
    storage.destroy(uid)
    find_active_plant(uid).stop()
    del (plants[uid])