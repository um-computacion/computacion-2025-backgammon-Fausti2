import unittest
from core.dice import Dice

class TestDice(unittest.TestCase):

    """
    Pruebas para la clase Dice.
    Se cubren tiradas, estado inicial, seteo manual de valores y validaciones.
    """

    def setUp(self):
        """
        Se ejecuta antes de cada test.
        Crea un objeto Dice nuevo.
        """
        self.dice = Dice()

    def test_roll_returns_values(self):
        """
        Al lanzar, los valores deben estar entre 1 y 6 y
        la cantidad debe ser 2 (normal) o 4 (dobles).
        """
        values = self.dice.roll()
        self.assertTrue(all(1 <= v <= 6 for v in values), "Los valores deben estar entre 1 y 6")
        self.assertIn(len(values), [2, 4], "Debe devolver 2 valores o 4 si son dobles")

    def test_get_values_after_roll(self):
        """
        Luego de lanzar, get_values() debe coincidir con lo almacenado internamente.
        """
        self.dice.roll()
        values = self.dice.get_values()
        self.assertEqual(values, self.dice._Dice__values)

    def test_initial_state_empty(self):
        """
        Antes de lanzar, get_values() debe devolver lista vacía.
        """
        self.assertEqual(self.dice.get_values(), [], "Al inicio no debe haber valores")

    def test_set_values_valido(self):
        """
        set_values() debe aceptar una lista de valores válidos (1..6).
        """
        self.dice.set_values([3, 4])
        self.assertEqual(self.dice.get_values(), [3, 4])

    def test_set_values_invalido(self):
        """
        set_values() debe lanzar ValueError si algún valor está fuera de 1..6.
        """
        with self.assertRaises(ValueError):
            self.dice.set_values([0, 7])
if __name__ == '__main__':
    unittest.main()  



   