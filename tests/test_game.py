import unittest
from core.board import Board
from core.player import Player
from core.dice import Dice
from core.game import BackgammonGame

class TestGame(unittest.TestCase):
    def setUp(self):
        """Crea tablero, jugadores, dados y el juego."""
        self.board = Board()
        self.white = Player("Blanco", "blanco")
        self.black = Player("Negro", "negro")
        self.dice = Dice()
        self.game = BackgammonGame(self.board, self.white, self.black, self.dice)

    def test_turno_inicial_es_blanco(self):
        """El jugador inicial debe ser blanco."""
        self.assertEqual(self.game.get_current_player().get_color(), "blanco")

    def test_cambio_de_turno(self):
        """end_turn() alterna el jugador actual."""
        self.game.end_turn()
        self.assertEqual(self.game.get_current_player().get_color(), "negro")
        self.game.end_turn()
        self.assertEqual(self.game.get_current_player().get_color(), "blanco")