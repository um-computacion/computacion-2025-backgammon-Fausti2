from typing import List, Dict
from core.checker import Checker

class Board:
  
    """
    Tablero de Backgammon con 24 puntos (0..23) y barra.
    Índices 0..23 recorren el tablero de un extremo a otro (orientación a definir).
    """

    def __init__(self):
        """Crea la estructura de puntos y barra, y deja el tablero vacío."""
        self.__points__: List[List[Checker]] = [[] for _ in range(24)]
        self.__bar__: Dict[str, List[Checker]] = {"blanco": [], "negro": []}
        self.setup_board()

    def setup_board(self):
     """Inicializa el tablero. Por ahora lo deja vacío, pero está preparado para cargar después la posición inicial estándar."""
     self.__points__ = [[] for _ in range(24)]
     self.__bar__ = {"blanco": [], "negro": []}

    # ---------- helpers básicos ----------
    def _check_index(self, idx: int) -> None:
        """Valida que el índice esté entre 0 y 23."""
        if not (0 <= idx < 24):
            raise IndexError("Índice de punto inválido (debe estar entre 0 y 23).")

    def get_points(self) -> List[List[Checker]]:
        """Devuelve la lista de puntos (referencia)."""
        return self.__points__

    def get_bar(self) -> Dict[str, List[Checker]]:
        """Devuelve la barra por color (referencia)."""
        return self.__bar__

    def get_point(self, idx: int) -> List[Checker]:
        """Devuelve la pila de fichas en el punto indicado."""
        self._check_index(idx)
        return self.__points__[idx]

    def count_at(self, idx: int) -> int:
        """Devuelve cuántas fichas hay en el punto indicado."""
        self._check_index(idx)
        return len(self.__points__[idx])

    def owner_at(self, idx: int) -> str | None:
        """Devuelve el color del punto o None si está vacío."""
        self._check_index(idx)
        stack = self.__points__[idx]
        if not stack:
            return None
        return stack[-1].get_color()

    def add_checker(self, idx: int, checker: Checker) -> None:
        """Agrega una ficha al punto indicado."""
        self._check_index(idx)
        self.__points__[idx].append(checker)

    def remove_checker(self, idx: int) -> Checker:
        """Quita y devuelve la ficha del tope en el punto indicado."""
        self._check_index(idx)
        if not self.__points__[idx]:
            raise ValueError("No hay fichas para retirar en ese punto.")
        return self.__points__[idx].pop()

    # ---------- barra del tablero: fichas capturadas pendientes ----------
    def send_to_bar(self, checker: Checker) -> None:
        """Envía una ficha a la barra según su color."""
        color = checker.get_color()
        if color not in self.__bar__:
            raise ValueError("Color inválido para la barra.")
        self.__bar__[color].append(checker)

    def pop_from_bar(self, color: str) -> Checker:
        """Saca y devuelve una ficha de la barra del color indicado."""
        if color not in self.__bar__:
            raise ValueError("Color inválido para la barra.")
        if not self.__bar__[color]:
            raise ValueError("No hay fichas en la barra de ese color.")
        return self.__bar__[color].pop()

    # ---------- movimientos simples (sin validar reglas) ----------
    def move_checker(self, start: int, end: int, checker: Checker) -> None:
        """
        Mueve una ficha de start a end (sin validar reglas).
        Valida índices y que la ficha esté en el origen.
        """
        self._check_index(start)
        self._check_index(end)
        if checker not in self.__points__[start]:
            raise ValueError("La ficha no está en el punto de origen.")
        self.__points__[start].remove(checker)
        self.__points__[end].append(checker)

    # ----------  Posición inicial de fichas  ----------
    def setup_standard(self) -> None:
        """Carga una posición inicial típica (ajustar según tu convención de índices).""" 
        self.setup_board()
        def drop(idx: int, color: str, n: int):
            for _ in range(n):
                self.__points__[idx].append(Checker(color))

        drop(0,  "blanco", 2)
        drop(11, "blanco", 5)
        drop(16, "blanco", 3)
        drop(18, "blanco", 5)

        drop(23, "negro", 2)
        drop(12, "negro", 5)
        drop(7,  "negro", 3)
        drop(5,  "negro", 5)

    def get_quadrant(self, idx: int) -> int:
        """Devuelve el número de cuadrante (1..4) del punto idx."""
        self._check_index(idx)
        if 0 <= idx <= 5:
            return 1
        if 6 <= idx <= 11:
            return 2
        if 12 <= idx <= 17:
            return 3
        return 4  # 18..23

    def to_ascii(self, niveles: int = 5) -> str:
        """
        Dibuja el tablero en ASCII con cuadrantes y pilas de fichas.
        - Fila superior: puntos 12..23 (pilas hacia abajo)
        - Fila inferior: puntos 11..00 (pilas hacia arriba)
        - Cada celda muestra hasta `niveles` fichas: B (blanco) / N (negro)
        - Muestra la barra y separadores de cuadrantes
        """
        def ch(color: str | None) -> str:
            return "B" if color == "blanco" else ("N" if color == "negro" else " ")

        top = list(range(12, 24))      # 3er y 4to cuadrante
        bot = list(range(11, -1, -1))  # 2do y 1er cuadrante

        def mk_row(indices: list[int], down: bool) -> list[str]:
            grid = [[" "]*len(indices) for _ in range(niveles)]
            for c, i in enumerate(indices):
                color = self.owner_at(i)
                h = min(len(self.get_point(i)), niveles)
                if h <= 0:
                    continue
                sym = ch(color)
                if down:
                    for r in range(h):            # llena 0..h-1
                        grid[r][c] = sym
                else:
                    for r in range(niveles-1, niveles-h-1, -1):  # llena desde abajo
                        grid[r][c] = sym
            return [" ".join(row) for row in grid]

          # Encabezados con separadores de cuadrantes
        def idx_line(indices: list[int]) -> str:
            parts = [f"{i:>2}" for i in indices]
            # separadores visuales entre cuadrantes (entre 17|18 y 5|6)
            if len(indices) == 12:
                parts.insert(6, "│")  # divide 6 y 6
            return " ".join(parts)

        top_idx = idx_line(top)
        bot_idx = idx_line(bot)

        top_rows = mk_row(top, down=True)
        bot_rows = mk_row(bot, down=False) 