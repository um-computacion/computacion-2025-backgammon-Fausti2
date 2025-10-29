import unittest
from unittest.mock import patch

from core.board import Board
from core.player import Player
from core.dice import Dice
from core.game import BackgammonGame
from core.checker import Checker


class TestGame(unittest.TestCase):
    def setUp(self):
        """Crea tablero, jugadores, dados y el juego."""
        self.board = Board()
        self.white = Player("Blanco", "blanco")
        self.black = Player("Negro", "negro")
        self.dice = Dice()
        self.game = BackgammonGame(self.board, self.white, self.black, self.dice)

    # ===================== Tests originales (con mínimos ajustes) =====================

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
        (Sin validar reglas complejas).
        """
        self.board.add_checker(0, Checker("blanco"))
        # Dados que habilitan 0 -> 5
        with patch.object(Dice, "roll", return_value=[5, 2]):
            self.game.roll_dice()
        self.game.move(0, 5, "blanco")
        self.assertEqual(len(self.board.get_point(0)), 0)
        self.assertEqual(len(self.board.get_point(5)), 1)
        self.assertEqual(self.board.owner_at(5), "blanco")

    def test_move_lanza_error_si_no_hay_ficha_en_origen(self):
        """Si no hay ficha del color en start, debe lanzar ValueError."""
        # Necesitamos tirada activa para no fallar por _require_roll()
        with patch.object(Dice, "roll", return_value=[5, 3]):
            self.game.roll_dice()
        with self.assertRaises(ValueError):
            self.game.move(0, 5, "blanco")

    def test_is_finished_placeholder_devuelve_false(self):
        """Hasta implementar borne-off, is_finished() debe ser False."""
        self.assertFalse(self.game.is_finished())

    # ===================== Nuevos tests para ampliar cobertura =====================

    def test_move_error_si_no_tiro_dados(self):
        """move() sin tirar dados primero debe fallar."""
        self.board.add_checker(0, Checker("blanco"))
        with self.assertRaises(ValueError):
            self.game.move(0, 3, "blanco")

    def test_move_error_color_equivocado(self):
        """Debe fallar si el color no coincide con el turno."""
        self.board.add_checker(0, Checker("blanco"))
        with patch.object(Dice, "roll", return_value=[3, 2]):
            self.game.roll_dice()
        with self.assertRaises(ValueError):
            self.game.move(0, 3, "negro")  # turno es blanco

    def test_move_direccion_incorrecta_blanco(self):
        """Blanco debe mover hacia índices mayores (end > start)."""
        self.board.add_checker(5, Checker("blanco"))
        with patch.object(Dice, "roll", return_value=[3, 2]):
            self.game.roll_dice()
        with self.assertRaises(ValueError):
            self.game.move(5, 3, "blanco")  # retroceder no permitido para blanco

    def test_move_direccion_incorrecta_negro(self):
        """Negro debe mover hacia índices menores (end < start)."""
        self.game.end_turn()  # turno negro
        self.board.add_checker(10, Checker("negro"))
        with patch.object(Dice, "roll", return_value=[3, 2]):
            self.game.roll_dice()
        with self.assertRaises(ValueError):
            self.game.move(10, 14, "negro")  # avanzar no permitido para negro

    def test_move_bloqueado_por_dos_oponentes(self):
        """No puede moverse a un punto con 2+ fichas rivales."""
        self.board.add_checker(0, Checker("blanco"))
        self.board.add_checker(5, Checker("negro"))
        self.board.add_checker(5, Checker("negro"))  # bloqueado
        with patch.object(Dice, "roll", return_value=[5, 1]):
            self.game.roll_dice()
        with self.assertRaises(ValueError):
            self.game.move(0, 5, "blanco")

    def test_move_comer_envia_a_barra(self):
        """Si hay 1 rival en destino, se lo come y lo manda a la barra."""
        self.board.add_checker(0, Checker("blanco"))
        self.board.add_checker(5, Checker("negro"))  # 1 rival
        with patch.object(Dice, "roll", return_value=[5]):
            self.game.roll_dice()
        bar_negro_antes = len(self.board.get_bar()["negro"])
        self.game.move(0, 5, "blanco")
        bar_negro_despues = len(self.board.get_bar()["negro"])
        self.assertEqual(bar_negro_despues, bar_negro_antes + 1)
        self.assertEqual(self.board.owner_at(5), "blanco")

    def test_entry_from_bar(self):
        """Con fichas en barra, solo se puede entrar desde -1 con un dado válido."""
        self.board.send_to_bar(Checker("blanco"))
        # 3 permite blanco entrar en 24-3 = 21
        with patch.object(Dice, "roll", return_value=[3, 6]):
            self.game.roll_dice()
        with self.assertRaises(ValueError):
            self.game.move(0, 21, "blanco")  # inválido: no desde barra
        self.game.move(-1, 21, "blanco")     # válido
        self.assertEqual(self.board.owner_at(21), "blanco")

    def test_bear_off_requiere_todas_en_home(self):
        """No se puede hacer bear-off si no están todas en el home."""
        self.board.add_checker(10, Checker("blanco"))  # fuera de 18..23
        self.board.add_checker(20, Checker("blanco"))
        with patch.object(Dice, "roll", return_value=[4, 2]):
            self.game.roll_dice()
        with self.assertRaises(ValueError):
            self.game.move(20, 24, "blanco")

    def test_bear_off_con_exacta_y_mayor(self):
        """Bear-off: exacta/mayor cuando corresponde."""
        # dos blancas en home: 18 y 20
        self.board.add_checker(18, Checker("blanco"))
        self.board.add_checker(20, Checker("blanco"))
        # una sola tirada que incluye 4 y 6
        with patch.object(Dice, "roll", return_value=[4, 6]):
            self.game.roll_dice()
        # 20 -> 24 con 4 (queda [6])
        self.game.move(20, 24, "blanco")
        # 18 -> 24 con 6 (queda sin dados, cambia turno)
        self.game.move(18, 24, "blanco")
        self.assertNotEqual(self.board.owner_at(18), "blanco")
        self.assertNotEqual(self.board.owner_at(20), "blanco")

    def test_legal_moves_y_can_play(self):
        """legal_moves devuelve algo coherente y can_play lo refleja."""
        self.board.add_checker(0, Checker("blanco"))
        with patch.object(Dice, "roll", return_value=[3]):
            self.game.roll_dice()
        moves = self.game.legal_moves()
        self.assertTrue(len(moves) >= 1)
        self.assertTrue(self.game.can_play())

    def test_consumo_de_dados_y_cambio_turno(self):
        """Al consumir todos los dados, debe pasar el turno."""
        self.board.add_checker(0, Checker("blanco"))
        with patch.object(Dice, "roll", return_value=[3]):
            self.game.roll_dice()
        self.game.move(0, 3, "blanco")
        self.assertEqual(self.game.get_rolled_values(), [])
        self.assertEqual(self.game.get_current_player().get_color(), "negro")


if __name__ == "__main__":
    unittest.main()
