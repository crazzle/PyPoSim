import time
import unittest

from plant.simple import SimplePlant


class SimplePlantTest(unittest.TestCase):

    def testDispatch(self):
        plant = SimplePlant.SimplePlant("1a", 100, 15, 5)
        new_state = plant.dispatch(75)
        time.sleep(1)
        end = new_state.evolve()
        self.assertTrue(end.setpoint == 95)

    def testDispatchReached(self):
        plant = SimplePlant.SimplePlant("1a", 100, 15, 5)
        new_state = plant.dispatch(90)
        time.sleep(1)
        next_state = new_state.evolve()
        time.sleep(1)
        end = next_state.evolve()
        self.assertTrue(end.setpoint == 90)

    def testEvolve(self):
        plant = SimplePlant.SimplePlant("1a", 100, 15, 5)
        new_state = plant.dispatch(50)
        time.sleep(1)
        first_evolved = new_state.evolve()
        time.sleep(1)
        second_evolved = first_evolved.evolve()
        self.assertTrue(second_evolved.setpoint == 90)

    def testEvolveLessOneSecond(self):
        plant = SimplePlant.SimplePlant("1a", 100, 15, 5)
        new_state = plant.dispatch(50)
        first_evolved = new_state.evolve()
        self.assertTrue(first_evolved.setpoint == 100)
        time.sleep(1)
        second_evolved = first_evolved.evolve()
        self.assertTrue(second_evolved.setpoint == 95)


if __name__ == "__main__":
    unittest.main()
