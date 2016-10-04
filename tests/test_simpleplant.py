import unittest
from plant import SimplePlant
import time


class SimplePlantTest(unittest.TestCase):

    def testDispatch(self):
        plant = SimplePlant.SimplePlant("1a", 100, 15, 5)
        new_state = plant.dispatch(150)
        time.sleep(1)
        end = new_state.evolve()
        self.assertTrue(end.power == 105)

    def testDispatchReached(self):
        plant = SimplePlant.SimplePlant("1a", 100, 15, 5)
        new_state = plant.dispatch(110)
        time.sleep(1)
        next_state = new_state.evolve()
        time.sleep(1)
        end = next_state.evolve()
        self.assertTrue(end.power == 110)

    def testEvolve(self):
        plant = SimplePlant.SimplePlant("1a", 100, 15, 5)
        new_state = plant.dispatch(150)
        time.sleep(1)
        first_evolved = new_state.evolve()
        time.sleep(1)
        second_evolved = first_evolved.evolve()
        self.assertTrue(second_evolved.power == 110)

    def testEvolveLessOneSecond(self):
        plant = SimplePlant.SimplePlant("1a", 100, 15, 5)
        new_state = plant.dispatch(150)
        first_evolved = new_state.evolve()
        self.assertTrue(first_evolved.power == 100)
        time.sleep(1)
        second_evolved = first_evolved.evolve()
        self.assertTrue(second_evolved.power == 105)


if __name__ == "__main__":
    unittest.main()
