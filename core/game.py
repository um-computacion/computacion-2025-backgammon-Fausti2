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

    def roll_dice(self) -> list[int]:
        """
        Tira los dados y guarda los valores del turno.
        Devuelve la lista de valores (2 o 4 si hay dobles).
        """
        self.__rolled__ = self.__dice__.roll()
        return self.__rolled__

    def get_rolled_values(self) -> list[int]:
        """Devuelve los valores de la tirada actual (si existen)."""
        return list(self.__rolled__) 
    
    def move(self, start: int, end: int, checker_color: str) -> None:
        """
        Mueve una ficha de 'start' a 'end' SIN validar reglas de Backgammon.
        Busca una ficha del color indicado en el punto 'start' y la mueve.
        Levanta ValueError si no encuentra ficha en el origen.
        """
        stack = self.__board__.get_point(start)
        # Busca una ficha del color solicitado en el punto de origen
        target = None
        for ch in stack:
            if ch.get_color() == checker_color:
                target = ch
                break
        if target is None:
            raise ValueError("No hay ficha del color indicado en el punto de origen.")
        self.__board__.move_checker(start, end, target)

    def is_finished(self) -> bool:
        """
        Indica si la partida terminó.
        TODO: implementar cuando se agregue borne-off y condición de victoria real.
        """
        return False 