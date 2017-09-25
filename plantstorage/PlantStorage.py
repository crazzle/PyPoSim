import sqlite3

from hashids import Hashids

import StoredPlant
import util.Config as Config
from plant.exception import PlantNotFoundException


class PlantStorage:

    def __init__(self):
        self.db = "plantstorage.db"
        self.id_generator = Hashids()

    def initialize_db(self):
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()

        if Config.get_startup_config()["clean_start"]:
            cursor.execute("""
            DROP TABLE IF EXISTS plant
            """)
            connection.commit()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS plant (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name varchar(255) NOT NULL,
          insertTS TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          capacity INTEGER NOT NULL,
          fluctuation INTEGER NOT NULL,
          ramp_in_seconds INTEGER NOT NULL
        )
        """)
        connection.commit()

    def get_all_plants(self):
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        rows = cursor.execute("select * from plant ORDER BY name, id ASC")
        connection.commit()
        entries = list()
        for row in rows:
            plant_id = self.id_generator.encode(row[0])
            name = row[1]
            capacity = row[3]
            fluctuation = row[4]
            ramp = row[5]
            entries.append(StoredPlant.StoredPlant(plant_id, name, capacity, fluctuation, ramp))
        return entries

    def get_plant_by_uid(self, uid):
        store_id = self.id_generator.decode(uid)
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        rows = cursor.execute("select * from plant where id=?", store_id)
        connection.commit()
        entries = list()
        for row in rows:
            plant_id = self.id_generator.encode(row[0])
            name = row[1]
            capacity = row[3]
            fluctuation = row[4]
            ramp = row[5]
            entries.append(StoredPlant.StoredPlant(plant_id, name, capacity, fluctuation, ramp))
        try:
            return entries[0]
        except IndexError:
            raise PlantNotFoundException.PlantNotFoundException("Plant not in storage", uid)

    def persist(self, name, capacity, fluctuation, ramp):
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        values = [name, capacity, fluctuation, ramp]
        cursor.execute("insert into plant(name,capacity,fluctuation,ramp_in_seconds) values (?,?,?,?)", values)
        connection.commit()
        return self.id_generator.encode(cursor.lastrowid)

    def destroy(self, plant_id):
        store_id = self.id_generator.decode(plant_id)
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        cursor.execute("delete from plant where id=?", store_id)
        connection.commit()

