from core.checker import Checker

class Player:
    """
    Representa un jugador de Backgammon.
    Cada jugador tiene un nombre, un color y 15 fichas.
    """

    def __init__(self, name: str, color: str):
        if color not in ("blanco", "negro"):
            raise ValueError("El color debe ser 'blanco' o 'negro'")
        
        self.__name = name
        self.__color = color
        self.__checkers = [Checker(color) for _ in range(15)]

    def get_name(self) -> str:
        return self.__name

    def get_color(self) -> str:
        return self.__color

    def get_checkers(self):
        return self.__checkers

    def set_name(self, name: str):
        self.__name = name

    def set_color(self, color: str):
        if color not in ("blanco", "negro"):
            raise ValueError("El color debe ser 'blanco' o 'negro'")
        self.__color = color
        # Actualizar color de las fichas si ya existen
        for checker in self.__checkers:
            checker.set_color(color)

    def set_checkers(self, checkers: list):
        self.__checkers = checkers

    def has_won(self) -> bool:
        """
        Para simplificar: un jugador gana si no tiene fichas en el tablero.
        (Esto se ajustará mejor cuando Board esté implementado).
        """
        return len(self.__checkers) == 0
