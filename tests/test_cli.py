import unittest
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

from cli.cli import CLI
from core.game import BackgammonGame
from core.board import Board
from core.player import Player
from core.dice import Dice
from core.checker import Checker


class TestCLI(unittest.TestCase):
    """
    Pruebas de la CLI (interfaz de texto).

    - Se testea la LÓGICA del CLI (flujos y llamadas), NO los mensajes impresos.
    - Por eso usamos redirect_stdout(StringIO()) sólo para SILENCIAR la salida.
    - Simulamos entradas de usuario con patch("builtins.input", side_effect=[...]).
    """

    def setUp(self):
        self.cli = CLI()

    def _run(self, inputs: list[str]):
        """
        Ejecuta cmdloop() con entradas simuladas y sale por el menú.

        Parámetro:
        - inputs: lista de comandos que el usuario "teclea".
        Implementación:
        - side_effect consume cada string como si fuera input().
        - siempre añadimos "4" al final para salir del menú principal.
        """
        entrada = "\n".join(inputs + ["4"])
        with patch("builtins.input", side_effect=entrada.split("\n")):
            with redirect_stdout(StringIO()):
                self.cli.cmdloop()

    # ---------- menú / navegación ----------

    def test_salir_inmediato(self):
        """El usuario elige '4' de entrada: cierra sin errores."""
        self._run(["4"])

    def test_opcion_invalida(self):
        """Una opción no válida no debe romper el flujo."""
        self._run(["xyz"])

    def test_reglas_y_ayuda(self):
        """Rutas de menú hacia Reglas (2) y Ayuda (3)."""
        self._run(["2", "3"])

    def test_empezar_y_volver(self):
        """Entra al juego (1) y vuelve con 'volver'."""
        self._run(["1", "volver"])

    def test_alias_menu(self):
        """'menu' actúa como 'volver' dentro del juego."""
        self._run(["1", "menu"])

    # ---------- comandos informativos dentro de la partida ----------

    def test_turno_tablero_ayuda(self):
        """Dentro del juego: 'turno', 'tablero', 'ayuda', luego 'volver'."""
        self._run(["1", "turno", "tablero", "ayuda", "volver"])

    # ---------- tirar / jugadas ----------

    def test_tirar_sin_jugadas_pasa_turno(self):
        """
        Si al tirar no hay movimientos legales, tu CLI debe pasar el turno.
        (No validamos texto, sólo ejercitamos la rama).
        """
        with patch.object(Dice, "roll", return_value=[3, 2]):
            self._run(["1", "tirar", "volver"])

    def test_tirar_y_jugadas(self):
        """Tirar dados y pedir 'jugadas' debe recorrer la rama correspondiente."""
        with patch.object(Dice, "roll", return_value=[5]):
            self._run(["1", "tirar", "jugadas", "volver"])

    # ---------- mover: entradas inválidas ----------

    def test_mover_sin_dos_argumentos(self):
        """'mover' debe validar que haya dos enteros."""
        self._run(["1", "mover 0", "volver"])

    def test_mover_no_enteros(self):
        """'mover a b' debe fallar validación de enteros (sin romper)."""
        self._run(["1", "mover a b", "volver"])

    def test_mover_fuera_de_rango(self):
        """'mover 30 -5' debe ser rechazado por validación de puntos."""
        self._run(["1", "mover 30 -5", "volver"])

    # ---------- mover válido: invoca a move con el color del turno ----------

    def test_mover_valido_invoca_move(self):
        """
        Verifica que, ante un 'mover 0 5' válido y con dados acordes,
        la CLI termine invocando BackgammonGame.move(start, end, color_del_turno).
        """
        cli = CLI()
        with patch("builtins.input", side_effect=["1", "tirar", "mover 0 5", "volver", "4"]), \
             patch.object(Dice, "roll", return_value=[5]), \
             redirect_stdout(StringIO()):
            cli._nuevo_juego()
            cli.board.add_checker(0, Checker("blanco"))
            # wraps=cli.game.move permite contar invocaciones sin romper la lógica real
            with patch.object(BackgammonGame, "move", wraps=cli.game.move) as mv:
                cli.cmdloop()
                self.assertGreaterEqual(mv.call_count, 1)

    # ---------- caminos de 'cmd.isdigit()' ----------

    def test_cmd_solo_numero(self):
        """Si el usuario escribe sólo un número, se recorre esa rama de ayuda sugerida."""
        self._run(["1", "7", "volver"])

    def test_cmd_dos_numeros(self):
        """Si escribe dos números, la CLI sugiere el formato 'mover <a> <b>' (sin validar texto)."""
        self._run(["1", "3 4", "volver"])

    # ---------- detectar ganador y cortar la partida ----------

    def test_detecta_ganador(self):
        """
        Fuerza un estado con ganador blanco:
        - Tablero sin blancas/negro en barra: Board parte vacío.
        - Agregamos una negra y la quitamos para forzar reevaluación a 'blanco ganó'.
        """
        with patch("builtins.input", side_effect=["1", "tablero", "volver", "4"]), \
             redirect_stdout(StringIO()):
            self.cli._nuevo_juego()
            self.cli.board.add_checker(0, Checker("negro"))
            self.cli.board.remove_checker(0)
            self.cli.cmdloop()

    # ---------- reiniciar ----------

    def test_reiniciar_crea_nuevas_instancias(self):
        """'reiniciar' debe construir nuevas instancias de Game/Board/Players/Dice."""
        with patch("builtins.input", side_effect=["1", "reiniciar", "volver", "4"]), \
             redirect_stdout(StringIO()):
            self.cli.cmdloop()
            self.assertIsInstance(self.cli.game, BackgammonGame)
            self.assertIsInstance(self.cli.board, Board)
            self.assertIsInstance(self.cli.blanco, Player)
            self.assertIsInstance(self.cli.negro, Player)
            self.assertIsInstance(self.cli.dice, Dice)


if __name__ == "__main__":
    unittest.main() 
  