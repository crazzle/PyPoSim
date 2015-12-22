import unittest
from plant import SimplePlant
import time


class SimplePlantTest(unittest.TestCase):

    def testDispatch(self):
        plant = SimplePlant.SimplePlant(100, 15, 5)
        new_state = plant.dispatch(150)
        self.assertTrue(new_state.power == 105)

    def testDispatchReached(self):
        plant = SimplePlant.SimplePlant(100, 15, 5)
        new_state = plant.dispatch(105)
        time.sleep(2)
        new_state.evolve()

    def testEvolve(self):
        plant = SimplePlant.SimplePlant(100, 15, 5)
        new_state = plant.dispatch(150)
        time.sleep(2)
        evolved_new = new_state.evolve()
        self.assertTrue(evolved_new.power == 110)


if __name__ == "__main__":
    unittest.main()
