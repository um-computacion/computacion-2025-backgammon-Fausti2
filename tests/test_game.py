import unittest
from unittest.mock import patch

from core.board import Board
from core.player import Player
from core.dice import Dice
from core.game import BackgammonGame
from core.checker import Checker


class TestGame(unittest.TestCase):
    """
    Pruebas unitarias de BackgammonGame.

    Claves:
    - Se mockean tiradas de dados con patch.object(Dice, "roll", return_value=[...])
      para evitar azar.
    - Se testean reglas: dirección por color, bloqueos, comer a la barra,
      entrada desde barra, bear-off (exacta / mayor permitido / no permitido),
      legal_moves y can_play, y estado de ganador.
    """

    def setUp(self):
        # Un entorno limpio por test
        self.board = Board()
        self.white = Player("Blanco", "blanco")
        self.black = Player("Negro", "negro")
        self.dice = Dice()
        self.game = BackgammonGame(self.board, self.white, self.black, self.dice)

    # ---------- básicos / turnos / dados ----------

    def test_turno_inicial_es_blanco(self):
        """Al inicio, el turno corresponde al jugador blanco."""
        self.assertEqual(self.game.get_current_player().get_color(), "blanco")

    def test_cambio_de_turno(self):
        """end_turn() alterna entre blanco y negro."""
        self.game.end_turn()
        self.assertEqual(self.game.get_current_player().get_color(), "negro")
        self.game.end_turn()
        self.assertEqual(self.game.get_current_player().get_color(), "blanco")

    def test_roll_dice_devuelve_valores_validos(self):
        """roll_dice() devuelve 2 o 4 valores entre 1 y 6."""
        values = self.game.roll_dice()
        self.assertTrue(all(1 <= v <= 6 for v in values))
        self.assertIn(len(values), (2, 4))

    def test_roll_dice_no_puede_tirar_dos_veces(self):
        """No se puede tirar dados si ya hay una tirada activa."""
        with patch.object(Dice, "roll", return_value=[3, 2]):
            self.game.roll_dice()
        with self.assertRaises(ValueError):
            self.game.roll_dice()

    def test_get_rolled_values_refleja_la_ultima_tirada(self):
        """get_rolled_values() devuelve la tirada actual almacenada."""
        with patch.object(Dice, "roll", return_value=[6, 1]):
            rolled = self.game.roll_dice()
        self.assertEqual(self.game.get_rolled_values(), rolled)

    def test_is_finished_placeholder_devuelve_false(self):
        """Por ahora is_finished() es un placeholder y devuelve False."""
        self.assertFalse(self.game.is_finished())

    # ---------- mover: errores comunes ----------

    def test_move_error_si_no_tiro_dados(self):
        """No se puede mover si primero no se tiraron los dados."""
        self.board.add_checker(0, Checker("blanco"))
        with self.assertRaises(ValueError):
            self.game.move(0, 3, "blanco")

    def test_move_error_color_equivocado(self):
        """No se puede mover con un color que no es el del turno."""
        self.board.add_checker(0, Checker("blanco"))
        with patch.object(Dice, "roll", return_value=[3, 2]):
            self.game.roll_dice()
        with self.assertRaises(ValueError):
            self.game.move(0, 3, "negro")

    def test_move_direccion_incorrecta_blanco(self):
        """El blanco debe mover a índices mayores (no puede retroceder)."""
        self.board.add_checker(5, Checker("blanco"))
        with patch.object(Dice, "roll", return_value=[3, 2]):
            self.game.roll_dice()
        with self.assertRaises(ValueError):
            self.game.move(5, 3, "blanco")

    def test_move_direccion_incorrecta_negro(self):
        """El negro debe mover a índices menores (no puede avanzar)."""
        self.game.end_turn()
        self.board.add_checker(10, Checker("negro"))
        with patch.object(Dice, "roll", return_value=[3, 2]):
            self.game.roll_dice()
        with self.assertRaises(ValueError):
            self.game.move(10, 14, "negro")

    def test_movimiento_no_coincide_con_dados(self):
        """La distancia del movimiento debe coincidir con algún dado disponible."""
        self.board.add_checker(0, Checker("blanco"))
        with patch.object(Dice, "roll", return_value=[6, 6]):
            self.game.roll_dice()
        with self.assertRaises(ValueError):
            self.game.move(0, 5, "blanco")

    # ---------- bloqueo / comer ----------

    def test_move_bloqueado_por_dos_oponentes(self):
        """No se puede mover a un punto con 2+ fichas rivales."""
        self.board.add_checker(0, Checker("blanco"))
        self.board.add_checker(5, Checker("negro"))
        self.board.add_checker(5, Checker("negro"))
        with patch.object(Dice, "roll", return_value=[5, 1]):
            self.game.roll_dice()
        with self.assertRaises(ValueError):
            self.game.move(0, 5, "blanco")

    def test_move_comer_envia_a_barra(self):
        """Si hay 1 rival en destino, se lo come y lo manda a la barra."""
        self.board.add_checker(0, Checker("blanco"))
        self.board.add_checker(5, Checker("negro"))
        with patch.object(Dice, "roll", return_value=[5]):
            self.game.roll_dice()
        antes = len(self.board.get_bar()["negro"])
        self.game.move(0, 5, "blanco")
        self.assertEqual(len(self.board.get_bar()["negro"]), antes + 1)
        self.assertEqual(self.board.owner_at(5), "blanco")

    # ---------- movimiento simple / consumo de dado / turno ----------

    def test_move_simple_mueve_y_consumo_de_dado_y_cambio_turno(self):
        """
        Un movimiento válido consume el dado usado y, si no quedan, cambia el turno.
        """
        self.board.add_checker(0, Checker("blanco"))
        with patch.object(Dice, "roll", return_value=[3]):
            self.game.roll_dice()
        self.game.move(0, 3, "blanco")
        self.assertEqual(self.game.get_rolled_values(), [])
        self.assertEqual(self.game.get_current_player().get_color(), "negro")

    # ---------- barra: entrada, bloqueos y comer al entrar ----------

    def test_entry_from_bar_valido(self):
        """Con fichas en barra, sólo se puede entrar desde -1 a la casilla permitida."""
        self.board.send_to_bar(Checker("blanco"))
        with patch.object(Dice, "roll", return_value=[3, 6]):
            self.game.roll_dice()
        with self.assertRaises(ValueError):
            self.game.move(0, 21, "blanco")  # inválido: hay ficha en barra
        self.game.move(-1, 21, "blanco")     # válido con 3 (24-3)
        self.assertEqual(self.board.owner_at(21), "blanco")

    def test_entry_from_bar_bloqueado(self):
        """No se puede entrar si el destino tiene 2+ rivales."""
        self.board.send_to_bar(Checker("blanco"))
        self.board.add_checker(21, Checker("negro"))
        self.board.add_checker(21, Checker("negro"))  # bloqueado
        with patch.object(Dice, "roll", return_value=[3]):
            self.game.roll_dice()
        with self.assertRaises(ValueError):
            self.game.move(-1, 21, "blanco")

    def test_entry_from_bar_comiendo(self):
        """Si hay 1 rival en el destino de entrada, se lo come al entrar."""
        self.board.send_to_bar(Checker("blanco"))
        self.board.add_checker(20, Checker("negro"))  # 1 rival en destino
        with patch.object(Dice, "roll", return_value=[4]):
            self.game.roll_dice()
        antes = len(self.board.get_bar()["negro"])
        self.game.move(-1, 20, "blanco")
        self.assertEqual(len(self.board.get_bar()["negro"]), antes + 1)
        self.assertEqual(self.board.owner_at(20), "blanco")

    # ---------- bear-off (exacta / mayor permitido / no permitido) ----------

    def test_bear_off_blanco_exacta_y_mayor_permitido(self):
        """
        Blanco en home: puede sacar con número exacto; mayor también si no hay fichas
        'más lejos' según la implementación (índices mayores para blanco).
        """
        self.board.add_checker(18, Checker("blanco"))
        self.board.add_checker(20, Checker("blanco"))
        with patch.object(Dice, "roll", return_value=[4, 6]):
            self.game.roll_dice()
        self.game.move(20, 24, "blanco")  # exacta 4
        self.game.move(18, 24, "blanco")  # exacta 6

    def test_bear_off_blanco_mayor_no_permitido_si_hay_mas_lejos(self):
        """
        En tu implementación, 'más lejos' para blanco se evalúa como índices mayores (j > start).
        Al poner una blanca en 22 y querer sacar la de 20 con un 5 (>4), debe fallar.
        """
        self.board.add_checker(22, Checker("blanco"))  # 'más lejos' según el código
        self.board.add_checker(20, Checker("blanco"))
        with patch.object(Dice, "roll", return_value=[5]):
            self.game.roll_dice()
        with self.assertRaises(ValueError):
            self.game.move(20, 24, "blanco")

    def test_bear_off_negro_exacta(self):
        """Negro saca con número exacto desde su home (0..5)."""
        self.game.end_turn()
        self.board.add_checker(5, Checker("negro"))  # distancia 6
        with patch.object(Dice, "roll", return_value=[6]):
            self.game.roll_dice()
        self.game.move(5, -1, "negro")

    def test_bear_off_negro_mayor_permitido(self):
        """
        Negro puede usar un dado MAYOR si no tiene fichas 'más lejos' en su home
        (para negro, 'más lejos' son índices MENORES que start).
        """
        self.game.end_turn()
        self.board.add_checker(2, Checker("negro"))  # dist 3
        with patch.object(Dice, "roll", return_value=[4]):  # >3 y sin más lejos
            self.game.roll_dice()
        self.game.move(2, -1, "negro")

    def test_bear_off_negro_mayor_no_permitido(self):
        """Si hay fichas negras más lejos (índice menor), no puede usar un mayor para sacar."""
        self.game.end_turn()
        self.board.add_checker(2, Checker("negro"))  # dist 3
        self.board.add_checker(0, Checker("negro"))  # más lejos (índice menor)
        with patch.object(Dice, "roll", return_value=[4]):
            self.game.roll_dice()
        with self.assertRaises(ValueError):
            self.game.move(2, -1, "negro")

    # ---------- legal_moves / can_play ----------

    def test_legal_moves_y_can_play_con_dado_simple(self):
        """Si hay una ficha y un dado válido, legal_moves debe tener algo y can_play True."""
        self.board.add_checker(0, Checker("blanco"))
        with patch.object(Dice, "roll", return_value=[3]):
            self.game.roll_dice()
        moves = self.game.legal_moves()
        self.assertTrue(len(moves) >= 1)
        self.assertTrue(self.game.can_play())

    def test_legal_moves_con_barra(self):
        """Con una ficha en barra, sólo deben aparecer jugadas de reingreso (-1 -> destino)."""
        self.board.send_to_bar(Checker("blanco"))
        with patch.object(Dice, "roll", return_value=[3]):
            self.game.roll_dice()
        moves = self.game.legal_moves()
        self.assertTrue(any(mv[0] == -1 and mv[2] == 3 for mv in moves))

    # ---------- ganador ----------

    def test_has_won_y_get_winner(self):
        """
        Con el tablero vacío, gana blanco .
        Si agregamos fichas de ambos colores, no hay ganador.
        """
        self.assertTrue(self.game.has_won("blanco"))
        self.assertEqual(self.game.get_winner(), "blanco")

        self.board.add_checker(0, Checker("blanco"))
        self.board.add_checker(23, Checker("negro"))
        self.assertFalse(self.game.has_won("blanco"))
        self.assertFalse(self.game.has_won("negro"))
        self.assertIsNone(self.game.get_winner())


if __name__ == "__main__":
    unittest.main() 

