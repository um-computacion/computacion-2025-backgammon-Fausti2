import unittest
from core.checker import Checker

class TestChecker(unittest.TestCase):
    """
    Conjunto de pruebas para la clase Checker.
    Verifica creación, acceso al color y validaciones.
    """

    def test_creacion_checker_blanco(self):
        ficha = Checker("blanco")
        self.assertEqual(ficha.get_color(), "blanco")

    def test_creacion_checker_negro(self): 
        """
        Debe crear una ficha negra correctamente.
        """
        ficha = Checker("negro")
        self.assertEqual(ficha.get_color(), "negro")

    def test_color_invalido(self):
        """
        Debe lanzar ValueError si se intenta crear con un color inválido.
        """
        with self.assertRaises(ValueError):
            Checker("rojo")

    def test_set_color_valido(self):
        """
        set_color() debe permitir cambiar el color a un valor válido.
        """
        ficha = Checker("blanco")
        ficha.set_color("negro")
        self.assertEqual(ficha.get_color(), "negro")

    def test_set_color_invalido(self):
        """
        set_color() debe lanzar ValueError si el color no es válido.
        """
        ficha = Checker("blanco")
        with self.assertRaises(ValueError):
            ficha.set_color("rojo") 

if __name__ == '__main__':
    unittest.main()          