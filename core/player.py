from core.checker import Checker

class Player:
    """
    Representa un jugador de Backgammon.
    Cada jugador tiene un nombre, un color y 15 fichas.
    """

    def __init__(self, name: str, color: str):
        if color not in ("blanco", "negro"):
            raise ValueError("El color debe ser 'blanco' o 'negro'")
        
        self.__name__ = name
        self.__color__ = color
        self.__checkers__ = [Checker(color) for _ in range(15)]

    def get_name(self) -> str:
        return self.__name__

    def get_color(self) -> str:
        return self.__color__

    def get_checkers(self):
        return self.__checkers__

    def has_won(self) -> bool:
        """
        Para simplificar: un jugador gana si no tiene fichas en el tablero.
        (Esto se ajustará mejor cuando Board esté implementado).
        """
        return len(self.__checkers__) == 0