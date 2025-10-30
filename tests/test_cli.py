import unittest
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

from cli.cli import CLI
from core.board import Board
from core.player import Player
from core.dice import Dice
from core.game import BackgammonGame 
from core.checker import Checker  


# -------------------- utilitarios tolerantes a distintas implementaciones --------------------

def _crear_juego(cli: CLI):
    """
    Intenta crear/iniciar un juego nuevo usando el método disponible en tu CLI.
    No valida mensajes, sólo dispara la lógica.
    """
    # Preferimos métodos explícitos si existen
    if hasattr(cli, "nuevo_juego"):
        return getattr(cli, "nuevo_juego")()
    if hasattr(cli, "_nuevo_juego"):
        return getattr(cli, "_nuevo_juego")()
    if hasattr(cli, "start_new_game"):
        return getattr(cli, "start_new_game")()
    # Fallback: muchos CLIs piden nombres por input en do_start
    if hasattr(cli, "do_start"):
        with patch("builtins.input", side_effect=["Jugador1", "Jugador2"]):
            return cli.do_start("")
    # Si no hay nada, último intento: método genérico 'start'
    if hasattr(cli, "start"):
        return getattr(cli, "start")()
    raise AssertionError("No encontré cómo iniciar un juego en CLI (faltan nuevo_juego/_nuevo_juego/do_start).")


def _reiniciar_juego(cli: CLI):
    """
    Intenta reiniciar la partida usando el método disponible en tu CLI.
    """
    for nombre in ("reiniciar", "_reiniciar", "reset", "do_reiniciar"):
        if hasattr(cli, nombre):
            m = getattr(cli, nombre)
            try:
                # algunos commands 'do_*' esperan un string arg
                return m("") if nombre.startswith("do_") else m()
            except TypeError:
                return m()
    # si tu CLI no define reinicio, simplemente volvemos a crear
    return _crear_juego(cli)


def _get_game(cli: CLI) -> BackgammonGame:
    """
    Obtiene el objeto juego que maneja la CLI, tolerando distintos nombres/visibilidades.
    """
    # acceso directo a atributo
    for attr in ("game", "_game", "__game__"):
        if hasattr(cli, attr):
            g = getattr(cli, attr)
            if isinstance(g, BackgammonGame):
                return g
    # getter
    if hasattr(cli, "get_game"):
        g = cli.get_game()
        if isinstance(g, BackgammonGame):
            return g
    raise AssertionError("La CLI no expone el BackgammonGame (game/_game/__game__ o get_game()).")


class TestCLI(unittest.TestCase):
    def setUp(self):
        # Capturamos stdout sólo para no ensuciar el runner (no se asertan mensajes)
        self.stdout = StringIO()
        with redirect_stdout(self.stdout):
            self.cli = CLI()
            # intentamos dejar un juego listo para inspeccionar
            try:
                _crear_juego(self.cli)
            except AssertionError:
                # si no hay manera, algunos CLIs crean el juego en el __init__ y ya está
                pass

    # -------------------- Tests de lógica (no mensajes) --------------------

    def test_crear_juego_instancias_basicas(self):
        """Crear juego debe dejar instancias válidas de Game/Board/Players/Dice."""
        with redirect_stdout(self.stdout):
            _crear_juego(self.cli)
        g = _get_game(self.cli)
        self.assertIsInstance(g, BackgammonGame)
        self.assertIsInstance(g.get_board(), Board)
        self.assertIsInstance(g.get_current_player(), Player)
        # el oponente también debe ser Player
        self.assertIsInstance(g.get_opponent(), Player)
        # y el juego debe tener dados
        # (si no hay getter, probamos un roll para evidenciar que hay Dice conectado)
        vals = g.roll_dice()
        self.assertIn(len(vals), (2, 4))
        for v in vals:
            self.assertTrue(1 <= v <= 6)

    def test_reiniciar_reemplaza_instancias(self):
        """Reiniciar debe crear nuevas instancias (no referenciar las anteriores)."""
        with redirect_stdout(self.stdout):
            _crear_juego(self.cli)
        g1 = _get_game(self.cli)
        b1 = g1.get_board()
        p1 = g1.get_current_player()
        # reiniciar
        with redirect_stdout(self.stdout):
            _reiniciar_juego(self.cli)
        g2 = _get_game(self.cli)
        b2 = g2.get_board()
        p2 = g2.get_current_player()

        # No deben ser los mismos objetos en memoria
        self.assertIsNot(g1, g2)
        self.assertIsNot(b1, b2)
        self.assertIsNot(p1, p2)
        # y deben seguir siendo del tipo correcto
        self.assertIsInstance(g2, BackgammonGame)
        self.assertIsInstance(b2, Board)
        self.assertIsInstance(p2, Player)

    def test_cmdloop_no_crashea_salir_inmediato(self):
        """
        Si tu CLI implementa cmdloop con un prompt de opciones, simular 'salir'
        para asegurar que no explota. Si no existe, se omite silenciosamente.
        """
        if hasattr(self.cli, "cmdloop"):
            with patch("builtins.input", side_effect=["4"]), redirect_stdout(self.stdout):
                try:
                    self.cli.cmdloop()
                except Exception as e:
                    self.fail(f"cmdloop arrojó excepción inesperada: {e}")

    def test_do_play_si_existe_no_crashea(self):
        """
        Si existe un comando do_play en la CLI, invocarlo y verificar que no
        arroja excepciones (la lógica interna del turno se testea en core).
        """
        if hasattr(self.cli, "do_play"):
            with redirect_stdout(self.stdout):
                try:
                    self.cli.do_play("")
                except Exception as e:
                    self.fail(f"do_play lanzó excepción inesperada: {e}")


if __name__ == "__main__":
    unittest.main() 
