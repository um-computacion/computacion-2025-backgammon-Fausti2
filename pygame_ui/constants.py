"""
Constantes de la UI (versión simple):
- Marco exterior color único
- Barra central y bandeja lateral con el mismo estilo
- Números y textos con color uniforme
"""

# Ventana
WIDTH, HEIGHT = 1000, 680
MARGIN = 18

# Tablero
BOARD_W, BOARD_H = WIDTH - 2 * MARGIN, HEIGHT - 2 * MARGIN

# Geometría: 12 columnas + canal + bandeja
POINT_W = BOARD_W // 14
BAR_W   = int(POINT_W * 1.20)   # barra central (comidas)
TRAY_W  = int(POINT_W * 1.10)   # bandeja lateral (bear-off)

# Apilado
STACK_H = (BOARD_H // 2) - 58
LAYER_H = max(14, STACK_H // 5)
DICE_SIZE = 46

# Paleta simple
FRAME_COLOR   = (96, 72, 48)     # marco exterior (único color)
BOARD_BG      = (224, 203, 170)  # base del tablero
TRI_A         = (165, 40, 35)    # rojo
TRI_B         = (118, 138, 78)   # verde

# Canal (barra) y bandeja: mismo estilo
CHANNEL_BG    = (210, 196, 170)  # rectángulo liso
CHANNEL_EDGE  = (120, 105, 85)   # borde fino (opcional)

# Fichas
WHITE       = (245, 245, 245)
WHITE_EDGE  = (220, 220, 220)
BLACK       = (35, 35, 35)
BLACK_EDGE  = (15, 15, 15)

# Textos (uniforme)
TEXT_UNI    = (35, 35, 35)
HILIGHT     = (80, 160, 255)
ERROR       = (170, 40, 40)

# Varias
FPS = 60
FONT_SIZE = 20
IDX_FROM_BAR = -1
CHECKERS_PER_COLOR = 15

# Ubicación de dados: "canal" (por defecto) o "topleft"
DICE_PLACEMENT = "canal"

# --- helpers ---
def x_col(k: int) -> int:
    """X de la columna lógica k (0..11); añade el hueco del canal central."""
    base = MARGIN + k * POINT_W
    if k >= 6:
        base += BAR_W
    return base
