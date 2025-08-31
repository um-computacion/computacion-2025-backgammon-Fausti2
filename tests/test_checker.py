import unittest
from core.checker import Checker

class TestChecker(unittest.TestCase):

    def test_creacion_checker_blanco(self):
        ficha = Checker("blanco")
        self.assertEqual(ficha.get_color(), "blanco")

    def test_creacion_checker_negro(self):
        ficha = Checker("negro")
        self.assertEqual(ficha.get_color(), "negro")

    def test_color_invalido(self):
        with self.assertRaises(ValueError):
            Checker("rojo")  
