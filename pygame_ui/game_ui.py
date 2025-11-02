"""
UI principal Pygame (corta y SOLID):
- Recibe opcionalmente un `game` (inyección). Si no, crea uno por defecto.
- Eventos mínimos: T/R/H/J + click origen→destino (y desde barra directo).
- Delegación de dibujo al BoardRenderer.
"""

import sys
try:
    import pygame # type: ignore 
except ImportError:
    print("ERROR: Pygame no está instalado. Ejecuta: pip install pygame"); sys.exit(1)

from .constants import *
from .renderer import BoardRenderer

class BackgammonUI:
    def __init__(self, game=None):
        pygame.init()
        pygame.display.set_caption("Backgammon (Pygame)")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock  = pygame.time.Clock()
        self.font   = pygame.font.SysFont(None, FONT_SIZE)

        # DI opcional: si no me dan un game, lo creo (compatibilidad con tu repo)
        if game is None:
            from core.board import Board
            from core.player import Player
            from core.dice import Dice
            from core.game import BackgammonGame
            b = Board(); b.setup_standard()
            w = Player("Blanco", "blanco"); n = Player("Negro", "negro")
            from core.dice import Dice
            game = BackgammonGame(b, w, n, Dice())
        self.game = game

        self.renderer = BoardRenderer(self.screen, self.font)

        # estado UI
        self.last_msg = None
        self.selected_from = None
        self.show_help = False
        self.show_moves = False
        self.legal_moves_cache = []
        self.running = True

    # ------------------- eventos
    def _on_key(self, e):
        if e.key in (pygame.K_ESCAPE, pygame.K_q, pygame.K_v):
            self.running = False
        elif e.key == pygame.K_r:
            self._restart()
        elif e.key == pygame.K_t:
            self._roll()
        elif e.key == pygame.K_j:
            self.show_moves = not self.show_moves
            if self.show_moves:
                self.legal_moves_cache = list(self.game.legal_moves())
        elif e.key == pygame.K_h:
            self.show_help = not self.show_help

    def _on_click(self, pos):
        idx = self.renderer.hit_test(pos)
        if idx is None:
            return
        color = self.game.get_current_player().get_color()
        tiene_barra = len(self.game.get_board().get_bar()[color]) > 0

        if self.selected_from is None:
            # Si hay fichas en barra, permito click directo en destino
            if tiene_barra and idx != IDX_FROM_BAR:
                self._move(IDX_FROM_BAR, idx); return
            self.selected_from = idx; self.last_msg = None
        else:
            self._move(self.selected_from, idx); self.selected_from = None

    # ------------------- acciones
    def _restart(self):
        from core.board import Board
        from core.player import Player
        from core.dice import Dice
        from core.game import BackgammonGame
        b = Board(); b.setup_standard()
        self.game = BackgammonGame(b, Player("Blanco","blanco"), Player("Negro","negro"), Dice())
        self.last_msg=None; self.selected_from=None; self.show_moves=False; self.legal_moves_cache=[]

    def _roll(self):
        try:
            self.game.roll_dice(); self.last_msg=None
            color = self.game.get_current_player().get_color()
            if len(self.game.get_board().get_bar()[color]) > 0:
                self.legal_moves_cache = list(self.game.legal_moves()); self.show_moves=True
        except Exception as ex:
            self.last_msg = str(ex)

    def _move(self, start, end):
        if start == IDX_FROM_BAR:
            start = -1
        color = self.game.get_current_player().get_color()
        try:
            self.game.move(start, end, color); self.last_msg=None
            if not self.game.get_rolled_values():
                self.show_moves=False
        except Exception as ex:
            self.last_msg = str(ex)

    # ------------------- bucle/render
    def run(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: self.running = False
                elif e.type == pygame.KEYDOWN: self._on_key(e)
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1: self._on_click(e.pos)

            legal = self.legal_moves_cache if self.show_moves else []
            self.renderer.render(self.game, self.last_msg, self.selected_from, self.show_help, legal)
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()
