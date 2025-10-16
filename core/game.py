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
    
    def _require_turn_color(self, color: str) -> None:
        turno = self.__current__.get_color()
        if color != turno:
            raise ValueError(f"Es turno de {turno}. No puede mover {color}.")
    
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
        self._require_turn_color(checker_color)
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
        # --- validar el destino según reglas básicas ---
        opponent = "negro" if checker_color == "blanco" else "blanco"
        dest_count = self.__board__.count_at(end)
        dest_owner = self.__board__.owner_at(end)

        if dest_owner == opponent and dest_count >= 2:
            # Punto bloqueado por el rival
            raise ValueError(f"Punto bloqueado por {opponent}: {end} tiene {dest_count} fichas.")

        # Si hay exactamente 1 del rival, se “come”: va a la barra
        if dest_owner == opponent and dest_count == 1:
            capturada = self.__board__.remove_checker(end)
            self.__board__.send_to_bar(capturada)

        # Mueve la ficha seleccionada
        self.__board__.move_checker(start, end, target)

        # Elimina el dado usado
        self.__rolled__.remove(dist)
        # Si se usaron todos los dados, cambiar el turno
        if not self.__rolled__:
            self.end_turn()
    def _home_range(self, color: str) -> range:
        return range(18, 24) if color == "blanco" else range(0, 6)

    def _all_in_home(self, color: str) -> bool:
        rang = self._home_range(color)
        for i in range(24):
            owner = self.__board__.owner_at(i)
            if owner == color and i not in rang:
                return False
        # además no debe haber fichas de ese color en la barra
        return len(self.__board__.get_bar()[color]) == 0
    def _entry_point(self, color: str, die: int) -> int:
        if color == "blanco":
            return 24 - die  # 1->23 ... 6->18
        return die - 1       # negro: 1->0 ... 6->5

    def _has_on_bar(self, color: str) -> bool:
        return len(self.__board__.get_bar()[color]) > 0

    def is_finished(self) -> bool:
        """
        Indica si la partida terminó.
        """
        return False
    