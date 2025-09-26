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



    def test_set_name(self):
        jugador = Player("Fausti", "blanco")
        jugador.set_name("NuevoNombre")
        self.assertEqual(jugador.get_name(), "NuevoNombre")

    def test_set_color_actualiza_checkers(self):
        jugador = Player("Fausti", "blanco")
        jugador.set_color("negro")
        self.assertEqual(jugador.get_color(), "negro")
        # Verificamos que TODAS las fichas se actualicen
        self.assertTrue(all(c.get_color() == "negro" for c in jugador.get_checkers()))

    def test_has_won(self):
        jugador = Player("Fausti", "blanco")
        # Simulamos que ya no tiene fichas
        jugador._Player__checkers = []
        self.assertTrue(jugador.has_won())