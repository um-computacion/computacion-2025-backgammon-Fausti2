import unittest
from core.dice import Dice

class TestDice(unittest.TestCase):
    def setUp(self):
        self.dice = Dice()

    def test_roll_returns_values(self):
        values = self.dice.roll()
        self.assertTrue(all(1 <= v <= 6 for v in values), "Los valores deben estar entre 1 y 6")
        self.assertIn(len(values), [2, 4], "Debe devolver 2 valores o 4 si son dobles")

    def test_get_values_after_roll(self):
        self.dice.roll()
        values = self.dice.get_values()
        self.assertEqual(values, self.dice._Dice__values)

    def test_initial_state_empty(self):
        self.assertEqual(self.dice.get_values(), [], "Al inicio no debe haber valores")

if __name__ == '__main__':
    unittest.main()  



   