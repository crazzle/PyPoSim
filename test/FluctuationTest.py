import unittest
from mathutil import Fluctuation


class FluctuationTest(unittest.TestCase):

    def testCalculation(self):
        baseline = 10
        value = 10
        percentage = 40
        relative_value = 4
        generator = Fluctuation.Fluctuation(percentage, baseline)

        for i in range(0, 100):
            result = generator.generate(value)
            self.assertTrue(-relative_value <= result <= relative_value)

    def testGetRelativeValue(self):
        baseline = 10
        value = 10
        percentage = 40
        generator = Fluctuation.Fluctuation(percentage, baseline)
        result = generator.get_relative_value(value)
        self.assertTrue(result == 4)

if __name__ == "__main__":
    unittest.main()
