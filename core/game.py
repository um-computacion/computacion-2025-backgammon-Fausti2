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
        """Tira los dados y guarda los valores del turno."""
        if self.__rolled__:
            raise ValueError("Ya hay una tirada activa; usá esos dados o pasá el turno.")
        self.__rolled__ = self.__dice__.roll()
        return self.__rolled__ 

    def get_rolled_values(self) -> list[int]:
        """Devuelve los valores de la tirada actual (si existen)."""
        return list(self.__rolled__) 
    
    def _require_roll(self) -> None:
        """Exige que haya una tirada activa para poder mover."""
        if not self.__rolled__:
            raise ValueError("Primero tirá los dados (comando 'tirar').")

    def _move_distance(self, start: int, end: int, color: str) -> int:
        """Calcula la distancia y valida dirección básica por color."""
        if color == "blanco":
            if end <= start:
                raise ValueError("El blanco debe mover hacia índices mayores (end > start).")
            return end - start
        if color == "negro":
            if end >= start:
                raise ValueError("El negro debe mover hacia índices menores (end < start).")
            return start - end
        raise ValueError("Color inválido. Usá 'blanco' o 'negro'.") 
    
    
    def move(self, start: int, end: int, checker_color: str) -> None:
        """
        Mueve una ficha de 'start' a 'end'.
        Busca una ficha del color indicado en el punto 'start' y la mueve.
        Levanta ValueError si no encuentra ficha en el origen.
        """
        self._require_roll()
        dist = self._move_distance(start, end, checker_color)
        if dist not in self.__rolled__:
           raise ValueError(f"El movimiento ({dist}) no coincide con la tirada: {self.__rolled__}")
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
        self.__rolled__.remove(dist) 
        # si no quedan dados → pasar turno automático
        if not self.__rolled__:
            self.end_turn()

    def is_finished(self) -> bool:
        """
        Indica si la partida terminó.
        TODO: implementar cuando se agregue borne-off y condición de victoria real.
        """
        return False 
    