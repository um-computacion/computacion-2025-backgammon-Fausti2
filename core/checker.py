class Checker:
    def __init__(self, color: str):
        if color not in ("blanco", "negro"):
            raise ValueError("El color debe ser 'blanco' o 'negro'")
        self.color = color

    def get_color(self) -> str:
        return self.color
    