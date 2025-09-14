from typing import List, Dict
from core.checker import Checker

class Board:
    """
    Representa el tablero de Backgammon con 24 puntos (0..23) y la barra.
    Convención de índices (propuesta y documentada):
    - 0 .. 23 recorren el tablero de un extremo al otro.
    - La orientación exacta (qué lado es 'home' de cada color) la fijarás
      cuando implementes reglas; por ahora es solo estructura.
    """

    def __init__(self):
        # cada punto es una lista de fichas (top = último)
        self.__points__: List[List[Checker]] = [[] for _ in range(24)]
        # barra por color (fichas capturadas pendientes de reingreso)
        self.__bar__: Dict[str, List[Checker]] = {"blanco": [], "negro": []}
        self.setup_board()

    def setup_board(self):
        """
        Inicializa el tablero.
        Por ahora: vacío. (Dejar hook para posición inicial estándar).
        Si querés la posición real, ver 'setup_standard()' más abajo.
        """
        self.__points__ = [[] for _ in range(24)]
        self.__bar__ = {"blanco": [], "negro": []}

    # ---------- helpers básicos ----------
    def _check_index(self, idx: int) -> None:
        if not (0 <= idx < 24):
            raise IndexError("Índice de punto inválido (debe estar entre 0 y 23).")

    def get_points(self) -> List[List[Checker]]:
        """Devuelve la matriz de puntos (referencia)."""
        return self.__points__

    def get_bar(self) -> Dict[str, List[Checker]]:
        """Devuelve la barra por color (referencia)."""
        return self.__bar__

    def get_point(self, idx: int) -> List[Checker]:
        """Devuelve la lista (pila) de fichas en el punto idx."""
        self._check_index(idx)
        return self.__points__[idx]

    def count_at(self, idx: int) -> int:
        """Cantidad de fichas en el punto idx."""
        self._check_index(idx)
        return len(self.__points__[idx])

    def owner_at(self, idx: int) -> str | None:
        """
        Devuelve el color que 'posee' el punto:
        - 'blanco' o 'negro' si hay fichas y todas del mismo color.
        - None si está vacío.
        (Si mezclás colores, lo permitimos por ahora porque no hay reglas aplicadas).
        """
        self._check_index(idx)
        stack = self.__points__[idx]
        if not stack:
            return None
        return stack[-1].get_color()

    def add_checker(self, idx: int, checker: Checker) -> None:
        """Agrega una ficha al punto idx."""
        self._check_index(idx)
        self.__points__[idx].append(checker)

    def remove_checker(self, idx: int) -> Checker:
        """Quita y devuelve la ficha del tope en el punto idx."""
        self._check_index(idx)
        if not self.__points__[idx]:
            raise ValueError("No hay fichas para retirar en ese punto.")
        return self.__points__[idx].pop()

    # ---------- barra (sin reglas, solo estructura) ----------
    def send_to_bar(self, checker: Checker) -> None:
        """Envía una ficha a la barra según su color."""
        color = checker.get_color()
        if color not in self.__bar__:
            raise ValueError("Color inválido para la barra.")
        self.__bar__[color].append(checker)

    def pop_from_bar(self, color: str) -> Checker:
        """Saca una ficha de la barra de 'color'."""
        if color not in self.__bar__:
            raise ValueError("Color inválido para la barra.")
        if not self.__bar__[color]:
            raise ValueError("No hay fichas en la barra de ese color.")
        return self.__bar__[color].pop()

    # ---------- movimientos simples (sin validar reglas) ----------
    def move_checker(self, start: int, end: int, checker: Checker) -> None:
        """
        Mueve 'checker' desde el punto 'start' al punto 'end' SIN validar reglas.
        - Valida índices.
        - Verifica que 'checker' esté en 'start'.
        """
        self._check_index(start)
        self._check_index(end)
        if checker not in self.__points__[start]:
            raise ValueError("La ficha no está en el punto de origen.")
        self.__points__[start].remove(checker)
        self.__points__[end].append(checker)

    # ---------- (opcional) posición estándar de Backgammon ----------
    def setup_standard(self) -> None:
        """
        Inicializa la disposición clásica (15 fichas por color).
        Necesita acordar una convención de índices.
        Ejemplo (documentá tu convención):
        - Blanco: 2 en 0, 5 en 11, 3 en 16, 5 en 18
        - Negro:  2 en 23,5 en 12, 3 en 7,  5 en 5
        (Esto depende de cómo numerás 0..23 en tu tablero).
        """
        self.setup_board()
        def drop(idx: int, color: str, n: int):
            for _ in range(n):
                self.__points__[idx].append(Checker(color))

        # Ajustá estas posiciones a tu convención
        drop(0,  "blanco", 2)
        drop(11, "blanco", 5)
        drop(16, "blanco", 3)
        drop(18, "blanco", 5)

        drop(23, "negro", 2)
        drop(12, "negro", 5)
        drop(7,  "negro", 3)
        drop(5,  "negro", 5)
