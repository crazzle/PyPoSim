import unittest
from mathutil import Fluctuation


class FluctuationTest(unittest.TestCase):

    def testCalculation(self):
        value = 10
        percentage = 40
        relative_value = 4
        generator = Fluctuation.Fluctuation(percentage)

        for i in range(0, 100):
            result = generator.generate(value)
            self.assertTrue(-relative_value <= result <= relative_value)

    def testGetRelativeValue(self):
        value = 10
        percentage = 40
        generator = Fluctuation.Fluctuation(percentage)
        result = generator.get_relative_value(value)
        self.assertTrue(result == 4)

if __name__ == "__main__":
    unittest.main()
