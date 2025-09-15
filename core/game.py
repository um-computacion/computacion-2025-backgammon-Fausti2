from core.board import Board
from core.player import Player
from core.dice import Dice

class BackgammonGame:
    """
    Coordina el flujo general del juego.
    Mantiene el tablero, los jugadores, los dados y el turno.
    """

    def __init__(self, board: Board, white: Player, black: Player, dice: Dice):
        """Inicializa la partida sin aplicar reglas todavía."""
        self.__board__ = board
        self.__white__ = white
        self.__black__ = black
        self.__dice__ = dice
        self.__current__ = white  # por ahora empieza blanco
        self.__rolled__ = []      # último resultado de dados

    def get_board(self) -> Board:
        """Devuelve el tablero."""
        return self.__board__

    def get_current_player(self) -> Player:
        """Devuelve el jugador de turno."""
        return self.__current__

    def get_opponent(self) -> Player:
        """Devuelve el oponente al jugador de turno."""
        return self.__black__ if self.__current__ == self.__white__ else self.__white__

    def end_turn(self) -> None:
        """Pasa el turno al otro jugador."""
        self.__current__ = self.get_opponent()
        self.__rolled__ = [] 