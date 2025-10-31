"""
Constantes de configuración para la interfaz de Pygame.
"""

# Dimensiones de ventana
WIDTH = 980
HEIGHT = 640
MARGIN = 20

# Dimensiones del tablero
BOARD_W = WIDTH - 2 * MARGIN
BOARD_H = HEIGHT - 2 * MARGIN

# Configuración de puntos y fichas
POINT_W = BOARD_W // 12
STACK_H = (BOARD_H // 2) - 40
LAYER_H = STACK_H // 5

# Colores
BG = (23, 26, 33)
BOARD_BG = (40, 44, 52)
WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
TRIANGLE_A = (197, 90, 17)
TRIANGLE_B = (181, 137, 0)
TEXT = (230, 230, 230)
HILIGHT = (90, 180, 255)
ERROR = (250, 120, 120)

# Configuración de juego
FPS = 60
FONT_SIZE = 18  
