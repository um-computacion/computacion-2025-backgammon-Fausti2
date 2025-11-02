import unittest
from core.board import Board
from core.checker import Checker


class TestBoard(unittest.TestCase):
    """
    Pruebas unitarias de la clase Board.
    """

    def setUp(self):
        # Cada test arranca con un tablero nuevo y vacío
        self.board = Board()

    # ---------- estado inicial / getters ----------

    def test_board_inicia_vacio(self):
        """Al crear el tablero, hay 24 puntos vacíos y la barra vacía por color."""
        points = self.board.get_points()
        bar = self.board.get_bar()
        self.assertEqual(len(points), 24)
        self.assertTrue(all(len(p) == 0 for p in points))
        self.assertEqual(bar, {"blanco": [], "negro": []})

    def test_owner_at_none_en_punto_vacio(self):
        """owner_at(idx) devuelve None cuando el punto está vacío."""
        self.assertIsNone(self.board.owner_at(7))

    # ---------- add/remove/move básicos ----------

    def test_add_y_remove_checker(self):
        """
        Agregar y quitar fichas en un punto:
        - add_checker(idx, checker)
        - remove_checker(idx) -> devuelve la ficha quitada
        """
        ficha = Checker("blanco")                 # creamos ficha blanca
        self.board.add_checker(0, ficha)          # la ponemos en el punto 0
        self.assertEqual(len(self.board.get_point(0)), 1)
        self.assertEqual(self.board.owner_at(0), "blanco")

        quitada = self.board.remove_checker(0)    # quitamos del punto 0
        self.assertIs(quitada, ficha)             # es la misma instancia
        self.assertEqual(len(self.board.get_point(0)), 0)
        self.assertIsNone(self.board.owner_at(0))

    def test_remove_checker_en_punto_vacio_levanta(self):
        """remove_checker(idx) en un punto vacío debe levantar ValueError."""
        with self.assertRaises(ValueError):
            self.board.remove_checker(3)

    def test_move_checker_valido(self):
        """move_checker() desplaza una ficha del origen al destino, validando índices."""
        ficha = Checker("negro")
        self.board.add_checker(0, ficha)
        self.board.move_checker(0, 5, ficha)
        self.assertEqual(len(self.board.get_point(0)), 0)
        self.assertEqual(len(self.board.get_point(5)), 1)
        self.assertEqual(self.board.owner_at(5), "negro")

    def test_move_checker_invalido_ficha_no_esta(self):
        """No se puede mover una ficha que NO está en el origen."""
        ficha = Checker("blanco")
        with self.assertRaises(ValueError):
            self.board.move_checker(0, 5, ficha)

    # ---------- barra ----------

    def test_send_and_pop_from_bar(self):
        """
        Enviar a barra y luego sacar:
        - send_to_bar(checker) la agrega a la barra por color.
        - pop_from_bar(color) la quita y devuelve.
        """
        ficha = Checker("negro")
        self.board.send_to_bar(ficha)
        self.assertIn(ficha, self.board.get_bar()["negro"])

        quitada = self.board.pop_from_bar("negro")
        self.assertIs(quitada, ficha)
        self.assertNotIn(quitada, self.board.get_bar()["negro"])

    def test_pop_from_bar_color_invalido(self):
        """pop_from_bar(color inválido) levanta ValueError."""
        with self.assertRaises(ValueError):
            self.board.pop_from_bar("verde")

    def test_pop_from_bar_vacio_levanta(self):
        """pop_from_bar(color) con barra vacía levanta ValueError."""
        with self.assertRaises(ValueError):
            self.board.pop_from_bar("blanco")

    def test_send_to_bar_color_invalido(self):
        """
        send_to_bar(checker) valida el color del checker a partir de checker.get_color().
        Doblamos un 'checker' trucho que responde 'verde' para forzar el error.
        """
        class FakeChecker:
            def get_color(self):
                return "verde"

        with self.assertRaises(ValueError):
            self.board.send_to_bar(FakeChecker())

    # ---------- índices inválidos ----------

    def test_get_point_indice_invalido(self):
        """get_point(idx) fuera de rango levanta IndexError."""
        for idx in (-1, 24, 999):
            with self.assertRaises(IndexError):
                self.board.get_point(idx)

    def test_add_checker_indice_invalido(self):
        """add_checker(idx, ...) fuera de rango levanta IndexError."""
        with self.assertRaises(IndexError):
            self.board.add_checker(-1, Checker("blanco"))
        with self.assertRaises(IndexError):
            self.board.add_checker(24, Checker("negro"))

    def test_remove_checker_indice_invalido(self):
        """remove_checker(idx) fuera de rango levanta IndexError."""
        with self.assertRaises(IndexError):
            self.board.remove_checker(-1)
        with self.assertRaises(IndexError):
            self.board.remove_checker(24)

    def test_move_checker_indices_invalidos(self):
        """move_checker() valida índices de origen y destino."""
        ficha = Checker("blanco")
        self.board.add_checker(0, ficha)
        with self.assertRaises(IndexError):
            self.board.move_checker(-1, 5, ficha)
        with self.assertRaises(IndexError):
            self.board.move_checker(0, 24, ficha)

    # ---------- setup inicial estándar ----------

    def test_setup_standard_totales_basicos(self):
        """
        setup_standard() coloca la apertura típica definida en tu Board.
        Verificamos total de fichas y algunos puntos clave.
        """
        self.board.setup_standard()
        total = sum(len(p) for p in self.board.get_points())
        self.assertEqual(total, 30)  # 15 por color

        self.assertEqual(len(self.board.get_point(0)), 2)    # 2 blancas
        self.assertEqual(len(self.board.get_point(23)), 2)   # 2 negras
        self.assertEqual(len(self.board.get_point(11)), 5)   # 5 blancas
        self.assertEqual(len(self.board.get_point(5)), 5)    # 5 negras

    # ---------- cuadrantes / ASCII ----------

    def test_get_quadrant_bordes(self):
        """get_quadrant() devuelve 1..4 correctamente en los bordes de cada rango."""
        self.assertEqual(self.board.get_quadrant(0), 1)
        self.assertEqual(self.board.get_quadrant(5), 1)
        self.assertEqual(self.board.get_quadrant(6), 2)
        self.assertEqual(self.board.get_quadrant(11), 2)
        self.assertEqual(self.board.get_quadrant(12), 3)
        self.assertEqual(self.board.get_quadrant(17), 3)
        self.assertEqual(self.board.get_quadrant(18), 4)
        self.assertEqual(self.board.get_quadrant(23), 4)

    def test_to_ascii_string_no_vacia(self):
        """to_ascii() devuelve un string con contenido (no vacío)."""
        s = self.board.to_ascii()
        self.assertIsInstance(s, str)
        self.assertGreater(len(s.strip()), 0)


if __name__ == "__main__":
    unittest.main() 
    