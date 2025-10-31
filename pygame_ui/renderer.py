"""
Módulo de renderizado del tablero de Backgammon.
"""

try:
    import pygame 
except ImportError:
    pygame = None

from .constants import *


class BoardRenderer:
    """Clase encargada de renderizar el tablero y las fichas."""
    
    def __init__(self, screen, font):
        if pygame is None:
            raise ImportError("Pygame no está instalado. Ejecuta: pip install pygame")
        
        self.screen = screen
        self.font = font
        self.hitmap = {}
    
    def _draw_triangle(self, rect, up=True, color=(200, 120, 40)):
        """Dibuja un triángulo en la posición especificada."""
        x, y, w, h = rect
        if up:
            pts = [(x, y), (x + w, y), (x + w / 2, y + h)]
        else:
            pts = [(x, y + h), (x + w, y + h), (x + w / 2, y)]
        pygame.draw.polygon(self.screen, color, pts)
    
    def _draw_text(self, text, pos, color=TEXT, center=False):
        """Dibuja texto en la posición especificada."""
        img = self.font.render(text, True, color)
        r = img.get_rect()
        if center:
            r.center = pos
        else:
            r.topleft = pos
        self.screen.blit(img, r)
    
    def _count_at_point(self, board):
        """
        Devuelve, para cada punto 0..23, (color_owner, count).
        """
        data = []
        for i in range(24):
            owner = board.owner_at(i)
            count = len(board.get_point(i))
            if owner is None or count == 0:
                data.append((None, 0))
            else:
                data.append((owner, count))
        return data
    
    def render(self, game, last_msg=None, selected_from=None):
        """
        Dibuja el tablero completo y devuelve un hitmap con las áreas clickeables.
        """
        self.screen.fill(BG)
        self.hitmap = {}
        
        # Fondo del tablero
        board_rect = pygame.Rect(MARGIN, MARGIN, BOARD_W, BOARD_H)
        pygame.draw.rect(self.screen, BOARD_BG, board_rect, border_radius=10)
        
        # Renderizar triángulos y crear hitmap
        self._render_triangles(selected_from)
        
        # Renderizar etiquetas de puntos
        self._render_labels()
        
        # Renderizar fichas
        self._render_pieces(game.get_board())
        
        # Renderizar HUD
        self._render_hud(game, last_msg)
        
        return self.hitmap
    
    def _render_triangles(self, selected_from):
        """Renderiza los triángulos del tablero y crea el hitmap."""
        # Parte superior: 11..0 (visual 12..1)
        for k, idx in enumerate(range(11, -1, -1)):
            x = MARGIN + k * POINT_W
            tri_rect = (x, MARGIN + 30, POINT_W, STACK_H)
            color = TRIANGLE_A if k % 2 == 0 else TRIANGLE_B
            self._draw_triangle(tri_rect, up=True, color=color)
            
            r = pygame.Rect(x, MARGIN, POINT_W, (BOARD_H // 2))
            self.hitmap[idx] = r
            
            if selected_from == idx:
                pygame.draw.rect(self.screen, HILIGHT, r, 2)
        
        # Parte inferior: 12..23 (visual 13..24)
        for k, idx in enumerate(range(12, 24)):
            x = MARGIN + k * POINT_W
            y = MARGIN + BOARD_H - 30 - STACK_H
            tri_rect = (x, y, POINT_W, STACK_H)
            color = TRIANGLE_B if k % 2 == 0 else TRIANGLE_A
            self._draw_triangle(tri_rect, up=False, color=color)
            
            r = pygame.Rect(x, MARGIN + BOARD_H // 2, POINT_W, (BOARD_H // 2))
            self.hitmap[idx] = r
            
            if selected_from == idx:
                pygame.draw.rect(self.screen, HILIGHT, r, 2)
    
    def _render_labels(self):
        """Renderiza las etiquetas numéricas de los puntos."""
        top_labels = [str(i) for i in range(12, 0, -1)]
        for k, s in enumerate(top_labels):
            cx = MARGIN + k * POINT_W + POINT_W // 2
            self._draw_text(s, (cx, MARGIN + 8), center=True)
        
        bot_labels = [str(i) for i in range(13, 25)]
        for k, s in enumerate(bot_labels):
            cx = MARGIN + k * POINT_W + POINT_W // 2
            self._draw_text(s, (cx, MARGIN + BOARD_H - 18), center=True)
    
    def _render_pieces(self, board):
        """Renderiza las fichas en el tablero."""
        counts = self._count_at_point(board)
        
        # Parte superior: 11..0
        for layer in range(5):
            for k, idx in enumerate(range(11, -1, -1)):
                owner, count = counts[idx]
                if count <= layer or owner is None:
                    continue
                
                cx = MARGIN + k * POINT_W + POINT_W // 2
                y0 = MARGIN + 30 + layer * LAYER_H + LAYER_H // 2
                rad = LAYER_H // 2 - 2
                col = WHITE if owner == "blanco" else BLACK
                
                pygame.draw.circle(self.screen, col, (cx, y0), max(6, rad))
                
                if layer == 4 and count > 5:
                    self._draw_text(str(count - 4), (cx, y0),
                                  center=True, color=HILIGHT)
        
        # Parte inferior: 12..23
        for layer in range(5):
            for k, idx in enumerate(range(12, 24)):
                owner, count = counts[idx]
                if count <= layer or owner is None:
                    continue
                
                cx = MARGIN + k * POINT_W + POINT_W // 2
                y_base = MARGIN + BOARD_H - 30
                y0 = y_base - layer * LAYER_H - LAYER_H // 2
                rad = LAYER_H // 2 - 2
                col = WHITE if owner == "blanco" else BLACK
                
                pygame.draw.circle(self.screen, col, (cx, y0), max(6, rad))
                
                if layer == 4 and count > 5:
                    self._draw_text(str(count - 4), (cx, y0),
                                  center=True, color=HILIGHT)
    
    def _render_hud(self, game, last_msg):
        """Renderiza el HUD con información del juego."""
        turno = game.get_current_player().get_color().capitalize()
        dados = game.get_rolled_values()
        
        self._draw_text(
            f"Turno: {turno}   Dados: {dados if dados else '-'}",
            (MARGIN + 6, HEIGHT - 28),
            color=TEXT
        )
        
        if last_msg:
            self._draw_text(last_msg, (MARGIN + 280, HEIGHT - 28), color=ERROR)
    
    def hit_test(self, pos):
        """Detecta qué punto del tablero fue clickeado."""
        for idx, rect in self.hitmap.items():
            if rect.collidepoint(pos):
                return idx
        return None 