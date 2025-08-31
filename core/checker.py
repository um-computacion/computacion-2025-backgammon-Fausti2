class Checker:
    def __init__(self, color: str):
        if color not in ("blanco", "negro"):
            raise ValueError("El color debe ser 'blanco' o 'negro'")
        self.__color  = color

    def get_color(self) -> str:
        return self.__color

    def set_color(self, color: str):
        if color not in ("blanco", "negro"):
            raise ValueError("El color debe ser 'blanco' o 'negro'")
        self.__color = color 