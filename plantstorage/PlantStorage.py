import sqlite3

from hashids import Hashids
import util.Config as Config
from plantexception import PlantNotFoundException
from plantstorage import StoredPlant


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
          power INTEGER NOT NULL,
          fluctuation INTEGER NOT NULL,
          ramp_in_seconds INTEGER NOT NULL
        )
        """)
        connection.commit()

    def get_all_plants(self):
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        rows = cursor.execute("select * from plant")
        connection.commit()
        entries = list()
        for row in rows:
            plant_id = self.id_generator.encode(row[0])
            name = row[1]
            power = row[3]
            fluctuation = row[4]
            ramp = row[5]
            entries.append(StoredPlant.StoredPlant(plant_id, name, power, fluctuation, ramp))
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
            power = row[3]
            fluctuation = row[4]
            ramp = row[5]
            entries.append(StoredPlant.StoredPlant(plant_id, name, power, fluctuation, ramp))
        try:
            return entries[0]
        except IndexError:
            raise PlantNotFoundException.PlantNotFoundException("Plant not in storage", uid)

    def persist(self, name, power, fluctuation, ramp):
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        values = [name, power, fluctuation, ramp]
        cursor.execute("insert into plant(name,power,fluctuation,ramp_in_seconds) values (?,?,?,?)", values)
        connection.commit()
        return self.id_generator.encode(cursor.lastrowid)

    def destroy(self, plant_id):
        store_id = self.id_generator.decode(plant_id)
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        cursor.execute("delete from plant where id=?", store_id)
        connection.commit()

