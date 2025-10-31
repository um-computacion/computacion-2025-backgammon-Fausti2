"""
Interfaz principal de usuario con Pygame para Backgammon.
"""

import sys
import pygame
from .constants import *
from .renderer import BoardRenderer


class BackgammonUI:
    """Clase principal que maneja la interfaz gráfica del juego."""
    
    def __init__(self, game):
        """
        Inicializa la interfaz gráfica.
        
        Args:
            game: Instancia de BackgammonGame
        """
        pygame.init()
        pygame.display.set_caption("Backgammon (Pygame)")
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        
        self.game = game
        self.renderer = BoardRenderer(self.screen, self.font)
        
        self.last_msg = None
        self.selected_from = None
        self.running = True
    
    def handle_events(self):
        """Procesa todos los eventos de Pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event)
    
    def _handle_keydown(self, event):
        """Maneja los eventos de teclado."""
        if event.key in (pygame.K_ESCAPE, pygame.K_q):
            self.running = False
        
        elif event.key == pygame.K_r:
            self._restart_game()
        
        elif event.key == pygame.K_t:
            self._roll_dice()
        
        elif event.key == pygame.K_j:
            self._show_legal_moves()
    
    def _handle_click(self, event):
        """Maneja los clicks del mouse en el tablero."""
        idx = self.renderer.hit_test(event.pos)
        
        if idx is not None:
            if self.selected_from is None:
                # Primer click: seleccionar origen
                self.selected_from = idx
                self.last_msg = None
            else:
                # Segundo click: intentar mover
                self._try_move(self.selected_from, idx)
                self.selected_from = None
    
    def _restart_game(self):
        """Reinicia el juego a su estado inicial."""
        from core.board import Board
        from core.player import Player
        from core.dice import Dice
        from core.game import BackgammonGame
        
        board = Board()
        board.setup_standard()
        white = Player("Blanco", "blanco")
        black = Player("Negro", "negro")
        dice = Dice()
        
        self.game = BackgammonGame(board, white, black, dice)
        self.last_msg = None
        self.selected_from = None
    
    def _roll_dice(self):
        """Tira los dados."""
        try:
            self.game.roll_dice()
            self.last_msg = None
        except Exception as ex:
            self.last_msg = str(ex)
    
    def _show_legal_moves(self):
        """Muestra las jugadas legales en consola (debug)."""
        print("Jugadas legales:", self.game.legal_moves())
    
    def _try_move(self, origen, destino):
        """Intenta realizar un movimiento."""
        color = self.game.get_current_player().get_color()
        try:
            self.game.move(origen, destino, color)
            self.last_msg = None
        except Exception as ex:
            self.last_msg = str(ex)
    
    def render(self):
        """Renderiza el frame actual."""
        self.renderer.render(self.game, self.last_msg, self.selected_from)
        pygame.display.flip()
    
    def run(self):
        """Loop principal del juego."""
        while self.running:
            self.handle_events()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Punto de entrada para ejecutar el juego con UI de Pygame."""
    from core.board import Board
    from core.player import Player
    from core.dice import Dice
    from core.game import BackgammonGame
    
    # Crear el juego
    board = Board()
    board.setup_standard()
    white = Player("Blanco", "blanco")
    black = Player("Negro", "negro")
    dice = Dice()
    game = BackgammonGame(board, white, black, dice)
    
    # Crear y ejecutar la interfaz
    ui = BackgammonUI(game)
    ui.run()


if __name__ == "__main__":
    main()