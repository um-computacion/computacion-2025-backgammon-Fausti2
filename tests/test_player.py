import unittest
from core.player import Player

class TestPlayer(unittest.TestCase):

    def test_creacion_jugador_blanco(self):
        jugador = Player("Fausti", "blanco")
        self.assertEqual(jugador.get_name(), "Fausti")
        self.assertEqual(jugador.get_color(), "blanco")
        self.assertEqual(len(jugador.get_checkers()), 15)

    def test_creacion_jugador_negro(self):
        jugador = Player("IA", "negro")
        self.assertEqual(jugador.get_color(), "negro")
        self.assertEqual(len(jugador.get_checkers()), 15)

    def test_color_invalido(self):
        with self.assertRaises(ValueError):
            Player("Error", "azul") 