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

    def test_roll_dice_devuelve_valores_validos(self):
        """roll_dice() debe devolver 2 o 4 valores entre 1 y 6."""
        values = self.game.roll_dice()
        self.assertTrue(all(1 <= v <= 6 for v in values))
        self.assertIn(len(values), (2, 4))

    def test_get_rolled_values_refleja_la_ultima_tirada(self):
        """get_rolled_values() iguala lo devuelto por roll_dice()."""
        rolled = self.game.roll_dice()
        self.assertEqual(self.game.get_rolled_values(), rolled)

    def test_move_simple_mueve_ficha_del_color(self):
        """
        Debe mover una ficha del color indicado del punto start al end.
        (Sin validar reglas: solo que la ficha exista en start).
        """
        # Preparo: pongo una ficha blanca en el punto 0
        from core.checker import Checker
        blanca = Checker("blanco")
        self.board.add_checker(0, blanca)

        # Muevo con el game
        self.game.move(0, 5, "blanco")

        # Verifico
        self.assertEqual(len(self.board.get_point(0)), 0)
        self.assertEqual(len(self.board.get_point(5)), 1)
        self.assertEqual(self.board.owner_at(5), "blanco")

    def test_move_lanza_error_si_no_hay_ficha_en_origen(self):
        """Si no hay ficha del color en start, debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.game.move(0, 5, "blanco")

    def test_is_finished_placeholder_devuelve_false(self):
        """Hasta implementar borne-off, is_finished() debe ser False."""
        self.assertFalse(self.game.is_finished()) 

if __name__ == "__main__":
    unittest.main()
    