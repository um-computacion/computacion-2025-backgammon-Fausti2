import unittest
from core.board import Board
from core.checker import Checker

class TestBoard(unittest.TestCase):
    """
    Pruebas para la clase Board.
    Verifica que la estructura del tablero y la barra funcionen correctamente.
    """

    def setUp(self):
        """
        Se ejecuta antes de cada test.
        Crea un tablero vacío.
        """
        self.board = Board()

    def test_board_inicia_vacio(self):
        """
        Al crear el tablero, los 24 puntos y la barra deben estar vacíos.
        """
        points = self.board.get_points()
        bar = self.board.get_bar()

        self.assertEqual(len(points), 24)  # Debe haber 24 puntos
        self.assertTrue(all(len(p) == 0 for p in points))  # Todos vacíos
        self.assertEqual(bar, {"blanco": [], "negro": []})  # Barra vacía

    def test_add_y_remove_checker(self):
        """
        Debe poderse agregar y quitar fichas en un punto.
        """
        ficha = Checker("blanco")
        self.board.add_checker(0, ficha)

        self.assertEqual(len(self.board.get_point(0)), 1)
        self.assertEqual(self.board.owner_at(0), "blanco")

        quitada = self.board.remove_checker(0)
        self.assertEqual(quitada, ficha)
        self.assertEqual(len(self.board.get_point(0)), 0)

    def test_move_checker_valido(self):
        """
        Debe mover una ficha de un punto a otro.
        """
        ficha = Checker("negro")
        self.board.add_checker(0, ficha)

        self.board.move_checker(0, 5, ficha)
        self.assertEqual(len(self.board.get_point(0)), 0)  # Se quitó de 0
        self.assertEqual(len(self.board.get_point(5)), 1)  # Se agregó en 5
        self.assertEqual(self.board.owner_at(5), "negro")

    def test_move_checker_invalido(self):
        """
        No debe permitir mover una ficha que no está en el punto de origen.
        """
        ficha = Checker("blanco")
        with self.assertRaises(ValueError):
            self.board.move_checker(0, 5, ficha)

    def test_send_and_pop_from_bar(self):
        """
        Debe poder enviar fichas a la barra y sacarlas después.
        """
        ficha = Checker("negro")
        self.board.send_to_bar(ficha)

        bar = self.board.get_bar()
        self.assertIn(ficha, bar["negro"])

        quitada = self.board.pop_from_bar("negro")
        self.assertEqual(quitada, ficha)
        self.assertNotIn(ficha, bar["negro"])