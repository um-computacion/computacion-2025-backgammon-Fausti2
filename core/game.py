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
        """Pasa el turno al otro jugador y limpia los dados."""
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

    # ----------------- validaciones auxiliares -----------------

    def _require_turn_color(self, color: str) -> None:
        turno = self.__current__.get_color()
        if color != turno:
            raise ValueError(f"Es turno de {turno}. No puede mover {color}.")

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

    # ----------------- reglas principales -----------------

    def move(self, start: int, end: int, checker_color: str) -> None:
        """
        Mueve una ficha de 'start' a 'end'.
        Busca una ficha del color indicado en el punto 'start' y la mueve.
        Levanta ValueError si no encuentra ficha en el origen.
        """
        self._require_roll()
        self._require_turn_color(checker_color)

        opponent = "negro" if checker_color == "blanco" else "blanco"

        # --- PRIORIDAD: si hay fichas en la barra, sólo se puede entrar ---
        if self._has_on_bar(checker_color):
            if start != -1:
                raise ValueError("Tenés fichas en la barra. Entrá con: mover -1 <destino> <color>.")

            # buscar un dado que haga coincidir la casilla de entrada
            dado_usado = None
            for d in sorted(set(self.__rolled__), reverse=True):
                if self._entry_point(checker_color, d) == end:
                    dado_usado = d
                    break
            if dado_usado is None:
                raise ValueError(f"Destino inválido para entrar desde barra con estos dados: {self.__rolled__}")

            # bloqueo/comer en el destino
            dest_count = self.__board__.count_at(end)
            dest_owner = self.__board__.owner_at(end)
            if dest_owner == opponent and dest_count >= 2:
                raise ValueError(f"Punto bloqueado por {opponent}: {end} tiene {dest_count} fichas.")
            if dest_owner == opponent and dest_count == 1:
                capt = self.__board__.remove_checker(end)
                self.__board__.send_to_bar(capt)

            # entrar: saco de la barra y coloco en 'end'
            ficha = self.__board__.pop_from_bar(checker_color)
            self.__board__.add_checker(end, ficha)

            # consumir dado y chequear fin de turno
            self.__rolled__.remove(dado_usado)
            if not self.__rolled__:
                self.end_turn()
            return

        # --- BEAR OFF: sacar fichas (end=24 blanco / end=-1 negro) ---
        is_bear_off = (
            (checker_color == "blanco" and end == 24) or
            (checker_color == "negro" and end == -1)
        )
        if is_bear_off:
            if not self._all_in_home(checker_color):
                raise ValueError("No podés sacar fichas: no están todas en tu cuadrante final.")

            # distancia necesaria para salir
            need = (24 - start) if checker_color == "blanco" else (start + 1)

            # dado exacto o mayor permitido (si no hay fichas más lejos en el home)
            if need in self.__rolled__:
                dado_usado = need
            else:
                home = self._home_range(checker_color)
                hay_mas_lejos = any(
                    self.__board__.owner_at(i) == checker_color and (
                        (checker_color == "blanco" and i > start) or
                        (checker_color == "negro" and i < start)
                    )
                    for i in home
                )
                if hay_mas_lejos:
                    raise ValueError(f"Necesitás exacto {need}; hay fichas más lejos en el home.")
                dado_usado = next((d for d in self.__rolled__ if d > need), None)
                if dado_usado is None:
                    raise ValueError(f"No hay dado exacto {need} ni mayor disponible: {self.__rolled__}")

            # quitar la ficha del punto (sale del tablero)
            stack = self.__board__.get_point(start)
            target = next((ch for ch in stack if ch.get_color() == checker_color), None)
            if target is None:
                raise ValueError("No hay ficha del color indicado en el punto de origen.")
            self.__board__.remove_checker(start)

            # consumir dado y chequear fin de turno, luego salir de move()
            self.__rolled__.remove(dado_usado)
            if not self.__rolled__:
                self.end_turn()
            return

        # --- MOVIMIENTO NORMAL ---
        dist = self._move_distance(start, end, checker_color)
        if dist not in self.__rolled__:
            raise ValueError(f"El movimiento ({dist}) no coincide con la tirada: {self.__rolled__}")

        # ficha del color en el origen
        stack = self.__board__.get_point(start)
        target = next((ch for ch in stack if ch.get_color() == checker_color), None)
        if target is None:
            raise ValueError("No hay ficha del color indicado en el punto de origen.")

        # validar destino (bloqueo/comer)
        dest_count = self.__board__.count_at(end)
        dest_owner = self.__board__.owner_at(end)
        if dest_owner == opponent and dest_count >= 2:
            raise ValueError(f"Punto bloqueado por {opponent}: {end} tiene {dest_count} fichas.")
        if dest_owner == opponent and dest_count == 1:
            capturada = self.__board__.remove_checker(end)
            self.__board__.send_to_bar(capturada)

        # mover
        self.__board__.move_checker(start, end, target)

        # consumir dado y, si no quedan, pasar turno
        self.__rolled__.remove(dist)
        if not self.__rolled__:
            self.end_turn()

    # ----------------- utilitarios de home/barra/ganador -----------------

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

    # ----------------- estado de finalización -----------------

    def is_finished(self) -> bool:
        """Indica si la partida terminó (placeholder: manejar desde CLI con has_won)."""
        return False

    def _any_on_board(self, color: str) -> bool:
        """¿Queda al menos una ficha de 'color' en algún punto 0..23?"""
        for i in range(24):
            if self.__board__.owner_at(i) == color:
                return True
        return False

    def has_won(self, color: str) -> bool:
        """
        Un color gana cuando no quedan fichas suyas en el tablero ni en la barra.
        (Las que se fueron por borne-off ya no están en el tablero.)
        """
        bar = self.__board__.get_bar()
        return not self._any_on_board(color) and len(bar[color]) == 0

    def get_winner(self) -> str | None:
        """Devuelve 'blanco' o 'negro' si ya ganó; si no hay ganador, None."""
        if self.has_won("blanco"):
            return "blanco"
        if self.has_won("negro"):
            return "negro"
        return None

    # devuelve [(start, end, die)] legales para el color al turno
    def legal_moves(self) -> list[tuple[int, int, int]]:
        color = self.__current__.get_color()
        dice = list(self.__rolled__)
        if not dice:
            return []

        opponent = "negro" if color == "blanco" else "blanco"
        moves: list[tuple[int, int, int]] = []

        # --- 1) PRIORIDAD: si hay fichas en la barra, sólo se puede entrar ---
        if self._has_on_bar(color):
            for d in set(dice):  # para can_play alcanza con 1 por valor
                end = self._entry_point(color, d)
                # destino válido si NO está bloqueado (0, propio, o 1 rival)
                dest_owner = self.__board__.owner_at(end)
                dest_count = self.__board__.count_at(end)
                blocked = (dest_owner == opponent and dest_count >= 2)
                if not blocked:
                    moves.append((-1, end, d))
            return moves

        # --- 2) BEAR-OFF disponible si todas en home ---
        all_home = self._all_in_home(color)

        # rango de índices según color/dirección
        pts = range(24) if color == "blanco" else range(23, -1, -1)

        for i in pts:
            if self.__board__.owner_at(i) != color:
                continue

            for d in set(dice):
                if color == "blanco":
                    end = i + d
                    # movimiento normal dentro del tablero
                    if 0 <= end <= 23:
                        dest_owner = self.__board__.owner_at(end)
                        dest_count = self.__board__.count_at(end)
                        if not (dest_owner == opponent and dest_count >= 2):
                            moves.append((i, end, d))
                    elif all_home and end == 24:
                        # exacto para salir
                        moves.append((i, 24, d))
                    elif all_home and end > 24:
                        # mayor permitido sólo si no hay fichas "más lejos" en home
                        hay_mas_lejos = any(
                            self.__board__.owner_at(j) == color and j > i
                            for j in self._home_range(color)
                        )
                        if not hay_mas_lejos:
                            moves.append((i, 24, d))

                else:  # negro
                    end = i - d
                    if 0 <= end <= 23:
                        dest_owner = self.__board__.owner_at(end)
                        dest_count = self.__board__.count_at(end)
                        if not (dest_owner == opponent and dest_count >= 2):
                            moves.append((i, end, d))
                    elif all_home and end == -1:
                        moves.append((i, -1, d))
                    elif all_home and end < -1:
                        hay_mas_lejos = any(
                            self.__board__.owner_at(j) == color and j < i
                            for j in self._home_range(color)
                        )
                        if not hay_mas_lejos:
                            moves.append((i, -1, d))

        return moves

    def can_play(self) -> bool:
        """Indica si el jugador al turno tiene al menos un movimiento legal con los dados activos."""
        return len(self.legal_moves()) > 0 
    