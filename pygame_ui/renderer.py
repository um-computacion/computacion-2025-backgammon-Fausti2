try:
    import pygame  # type: ignore
except ImportError:
    pygame = None

from .constants import *

# ---------------- util ----------------
def _txt(surf, text, pos, color=TEXT_UNI, center=False, font=None):
    font = font or pygame.font.SysFont(None, FONT_SIZE)
    img = font.render(text, True, color)
    r = img.get_rect()
    if center:
        r.center = pos
    else:
        r.topleft = pos
    surf.blit(img, r)

def _tri(surf, rect, up, color):
    x, y, w, h = rect
    pts = (
        [(x, y), (x + w, y), (x + w / 2, y + h)]
        if up
        else [(x, y + h), (x + w, y + h), (x + w / 2, y)]
    )
    pygame.draw.polygon(surf, color, pts)

def _chip(surf, x, y, face, edge, r):
    pygame.draw.circle(surf, edge, (x, y), r + 2)
    pygame.draw.circle(surf, face, (x, y), r)

def _pips(surf, rect, val):
    cx, cy = rect.center
    r = 4
    dx = rect.w // 4
    dy = rect.h // 4
    table = {
        1: [(cx, cy)],
        2: [(cx - dx, cy - dy), (cx + dx, cy + dy)],
        3: [(cx, cy), (cx - dx, cy - dy), (cx + dx, cy + dy)],
        4: [(cx - dx, cy - dy), (cx + dx, cy - dy), (cx - dx, cy + dy), (cx + dx, cy + dy)],
        5: [(cx, cy), (cx - dx, cy - dy), (cx + dx, cy - dy), (cx - dx, cy + dy), (cx + dx, cy + dy)],
        6: [
            (cx - dx, cy - dy), (cx, cy - dy), (cx + dx, cy - dy),
            (cx - dx, cy + dy), (cx, cy + dy), (cx + dx, cy + dy),
        ],
    }
    for p in table.get(val, []):
        pygame.draw.circle(surf, (30, 30, 30), p, r)

class BoardRenderer:
    def __init__(self, screen, font):
        if pygame is None:
            raise ImportError("Pygame no está instalado. pip install pygame")
        self.sc, self.font = screen, font
        self.hitmap = {}

    # ---------- pública ----------
    def render(self, game, last_msg=None, selected_from=None, show_help=False, legal_moves=None):
        legal_moves = legal_moves or []
        self.hitmap = {}
        self._board_and_areas()
        self._stacks_points(game)
        self._bar(game)
        self._tray(game)
        self._hud(game, last_msg, show_help, legal_moves)
        if selected_from is not None and selected_from in self.hitmap:
            pygame.draw.rect(self.sc, HILIGHT, self.hitmap[selected_from], 2)
        return self.hitmap

    def hit_test(self, pos):
        for i, r in self.hitmap.items():
            if r.collidepoint(pos):
                return i
        return None

    # ---------- tablero + hitmap + labels ----------
    def _board_and_areas(self):
        # marco + fondo interno (colores unificados)
        frame = pygame.Rect(MARGIN, MARGIN, BOARD_W, BOARD_H)
        pygame.draw.rect(self.sc, FRAME_COLOR, frame, border_radius=14)
        inner = frame.inflate(-16, -16)
        pygame.draw.rect(self.sc, BOARD_BG, inner, border_radius=10)  # << fijate: agregamos color

        # canal y bandeja: mismo estilo liso
        canal = pygame.Rect(MARGIN + 6 * POINT_W, MARGIN, BAR_W, BOARD_H)
        pygame.draw.rect(self.sc, CHANNEL_BG, canal, border_radius=6)
        pygame.draw.rect(self.sc, CHANNEL_EDGE, canal, 1, border_radius=6)  # borde fino
        self.hitmap[IDX_FROM_BAR] = canal

        tray_x = MARGIN + BOARD_W - TRAY_W
        self.tray = pygame.Rect(tray_x, MARGIN, TRAY_W, BOARD_H)
        pygame.draw.rect(self.sc, CHANNEL_BG, self.tray, border_radius=6)
        pygame.draw.rect(self.sc, CHANNEL_EDGE, self.tray, 1, border_radius=6)

        # triángulos + zonas clicables + labels (color de texto único)
        # top 11..0
        for k, idx in enumerate(range(11, -1, -1)):
            x = x_col(k)
            _tri(self.sc, (x, MARGIN + 28, POINT_W, STACK_H), True, TRI_A if k % 2 == 0 else TRI_B)
            self.hitmap[idx] = pygame.Rect(x, MARGIN, POINT_W, BOARD_H // 2)
            _txt(self.sc, str(12 - k), (x + POINT_W // 2, MARGIN + 6), TEXT_UNI, True)
        # bottom 12..23
        for k, idx in enumerate(range(12, 24)):
            x = x_col(k)
            y = MARGIN + BOARD_H - 28 - STACK_H
            _tri(self.sc, (x, y, POINT_W, STACK_H), False, TRI_B if k % 2 == 0 else TRI_A)
            self.hitmap[idx] = pygame.Rect(x, MARGIN + BOARD_H // 2, POINT_W, BOARD_H // 2)
            _txt(self.sc, str(13 + k), (x + POINT_W // 2, MARGIN + BOARD_H - 22), TEXT_UNI, True)

    # ---------- fichas en puntos ----------
    def _stacks_points(self, game):
        board = game.get_board()
        rad = LAYER_H // 2

        def draw_range(indices, top=True):
            for layer in range(5):
                for k, idx in enumerate(indices):
                    owner = board.owner_at(idx)
                    if not owner:
                        continue
                    cnt = len(board.get_point(idx))
                    if cnt <= layer:
                        continue
                    cx = x_col(k) + POINT_W // 2
                    y = (
                        MARGIN + 28 + layer * LAYER_H + rad
                        if top
                        else MARGIN + BOARD_H - 28 - layer * LAYER_H - rad
                    )
                    face, edge = (WHITE, WHITE_EDGE) if owner == "blanco" else (BLACK, BLACK_EDGE)
                    _chip(self.sc, cx, y, face, edge, rad)
                    if layer == 4 and cnt > 5:
                        _txt(self.sc, str(cnt - 4), (cx, y), TEXT_UNI, True)

        draw_range(range(11, -1, -1), top=True)
        draw_range(range(12, 24), top=False)

    # ---------- barra central (comidas) ----------
    def _bar(self, game):
        bar = game.get_board().get_bar()
        cnt_b, cnt_w = len(bar["negro"]), len(bar["blanco"])
        canal = pygame.Rect(MARGIN + 6 * POINT_W, MARGIN, BAR_W, BOARD_H)
        rad = LAYER_H // 2

        for i in range(min(cnt_b, 5)):
            _chip(self.sc, canal.centerx, MARGIN + 30 + i * (LAYER_H - 2), BLACK, BLACK_EDGE, rad)
        if cnt_b > 5:
            _txt(self.sc, str(cnt_b - 5), (canal.centerx, MARGIN + 30 + 5 * (LAYER_H - 2)), TEXT_UNI, True)

        for i in range(min(cnt_w, 5)):
            _chip(self.sc, canal.centerx, MARGIN + BOARD_H - 30 - i * (LAYER_H - 2), WHITE, WHITE_EDGE, rad)
        if cnt_w > 5:
            _txt(self.sc, str(cnt_w - 5), (canal.centerx, MARGIN + BOARD_H - 30 - 5 * (LAYER_H - 2)), TEXT_UNI, True)

    # ---------- bandeja lateral (solo n° de bear-off) ----------
    def _tray(self, game):
        board = game.get_board()

        def count_on_board(color):
            return sum(len(board.get_point(i)) for i in range(24) if board.owner_at(i) == color)

        cnt_w_bar, cnt_b_bar = len(board.get_bar()["blanco"]), len(board.get_bar()["negro"])
        off_w = max(0, CHECKERS_PER_COLOR - (count_on_board("blanco") + cnt_w_bar))
        off_b = max(0, CHECKERS_PER_COLOR - (count_on_board("negro") + cnt_b_bar))

        # Solo números (sin recuadros)
        bigf = pygame.font.SysFont(None, FONT_SIZE + 10)
        top_pos = (self.tray.centerx, self.tray.y + self.tray.h * 0.25)
        bot_pos = (self.tray.centerx, self.tray.y + self.tray.h * 0.75)
        _txt(self.sc, str(off_b), top_pos, TEXT_UNI, True, bigf)
        _txt(self.sc, str(off_w), bot_pos, TEXT_UNI, True, bigf)

    # ---------- HUD (turno + dados + ayudas/errores) ----------
    def _hud(self, game, last_msg, show_help, legal_moves):
        # “Turno de …” centrado en el cuadrante izquierdo
        p = game.get_current_player()
        nombre = p.get_name() if hasattr(p, "get_name") else p.get_color().capitalize()
        titlef = pygame.font.SysFont(None, FONT_SIZE + 10)
        left_center = (MARGIN + (BOARD_W - TRAY_W - BAR_W) // 4, MARGIN + BOARD_H // 2)
        _txt(self.sc, f"Turno de {nombre}", left_center, TEXT_UNI, True, titlef)

        # Dados en el canal central
        vals = game.get_rolled_values()
        if vals:
            canal = pygame.Rect(MARGIN + 6 * POINT_W, MARGIN, BAR_W, BOARD_H)
            w = h = DICE_SIZE
            gap = 10
            y0 = MARGIN + 44
            total = w * 2 + gap
            x0 = canal.centerx - total // 2
            boxes = [pygame.Rect(x0, y0, w, h), pygame.Rect(x0 + w + gap, y0, w, h)]
            for i, rc in enumerate(boxes):
                pygame.draw.rect(self.sc, (250, 250, 250), rc, border_radius=6)
                pygame.draw.rect(self.sc, (60, 60, 60), rc, 2, border_radius=6)
                if i < len(vals):
                    _pips(self.sc, rc, vals[i])

        # Destinos legales
        dests = {d for _, d, _ in legal_moves}
        for idx, rc in self.hitmap.items():
            if idx in dests:
                pygame.draw.rect(self.sc, HILIGHT, rc, 2)

        # Ayuda (opcional)
        if show_help:
            panel = pygame.Surface((520, 110), pygame.SRCALPHA)
            panel.fill((0, 0, 0, 140))
            lines = [
                "Controles:",
                "T: tirar   R: reiniciar   H: ayuda   J: jugadas",
                "Click: origen → destino. Con fichas en barra, podés clickear directo el destino.",
                "ESC/Q/V: volver al menú",
            ]
            y = 10
            for i, t in enumerate(lines):
                f = pygame.font.SysFont(None, FONT_SIZE + (6 if i == 0 else 0))
                panel.blit(f.render(t, True, (240, 240, 240)), (12, y))
                y += f.get_height() + 2
            self.sc.blit(panel, (MARGIN + 10, MARGIN + BOARD_H - 110 - 10))

        # Errores
        if last_msg:
            band = pygame.Surface((BOARD_W, 28), pygame.SRCALPHA)
            band.fill((*ERROR, 180))
            band.blit(self.font.render(str(last_msg), True, (255, 255, 255)), (10, 5))
            self.sc.blit(band, (MARGIN, MARGIN + BOARD_H - 30)) 