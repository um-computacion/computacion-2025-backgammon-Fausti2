"""
Módulo de interfaz gráfica con Pygame para Backgammon.
"""

try:
    from .game_ui import BackgammonUI
    __all__ = ['BackgammonUI']
except ImportError:
    # Si pygame no está instalado, no exportamos nada
    __all__ = []