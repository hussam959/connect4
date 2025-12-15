"""Game UI using Pygame"""

import pygame
from constants import *


class GameUI:
    def __init__(self):
        width = COLS * SQUARESIZE
        height = (ROWS + 1) * SQUARESIZE
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Connect4 - Player vs AI')

    def draw_board(self, board):
        """Draw the game board"""
        self.screen.fill(BLACK)

        # Draw blue grid
        for c in range(COLS):
            for r in range(ROWS):
                pygame.draw.rect(self.screen, BLUE,
                               (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, 
                                SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(self.screen, BLACK,
                                 (c*SQUARESIZE + SQUARESIZE//2, 
                                  (r+1)*SQUARESIZE + SQUARESIZE//2), RADIUS)

        # Draw pieces
        for c in range(COLS):
            for r in range(ROWS):
                if board[r][c] == 1:
                    pygame.draw.circle(self.screen, RED,
                                     (c*SQUARESIZE + SQUARESIZE//2, 
                                      (r+1)*SQUARESIZE + SQUARESIZE//2), RADIUS)
                elif board[r][c] == 2:
                    pygame.draw.circle(self.screen, YELLOW,
                                     (c*SQUARESIZE + SQUARESIZE//2, 
                                      (r+1)*SQUARESIZE + SQUARESIZE//2), RADIUS)

        pygame.display.update()

    def draw_button(self, text, rect, base_color, hover_color, is_hovered):
        """Draw a single button"""
        color = hover_color if is_hovered else base_color
        
        # Draw button background with shadow
        shadow_rect = rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(self.screen, (30, 30, 30), shadow_rect, border_radius=12)
        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        
        # Draw border
        border_color = WHITE if is_hovered else (150, 150, 150)
        pygame.draw.rect(self.screen, border_color, rect, 4, border_radius=12)
        
        # Draw text
        font = pygame.font.SysFont('Arial', 32, bold=True)
        label = font.render(text, True, WHITE)
        text_rect = label.get_rect(center=rect.center)
        self.screen.blit(label, text_rect)

    def show_game_over_screen(self, message, message_color):
        """Show game over screen with Try Again and Exit buttons"""
        # Draw semi-transparent overlay
        overlay = pygame.Surface(self.size)
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw winner message
        font_large = pygame.font.SysFont('Arial', 56, bold=True)
        label = font_large.render(message, True, message_color)
        msg_rect = label.get_rect(center=(self.size[0]//2, self.size[1]//2 - 100))
        
        # Draw message shadow
        shadow_label = font_large.render(message, True, (20, 20, 20))
        shadow_rect = msg_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        self.screen.blit(shadow_label, shadow_rect)
        self.screen.blit(label, msg_rect)
        
        # Button dimensions
        button_width = 200
        button_height = 70
        button_spacing = 30
        start_x = (self.size[0] - (button_width * 2 + button_spacing)) // 2
        button_y = self.size[1]//2 + 20
        
        try_again_rect = pygame.Rect(start_x, button_y, button_width, button_height)
        exit_rect = pygame.Rect(start_x + button_width + button_spacing, button_y, 
                               button_width, button_height)
        
        # Game loop for buttons
        waiting = True
        while waiting:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check hover state
            try_again_hover = try_again_rect.collidepoint(mouse_pos)
            exit_hover = exit_rect.collidepoint(mouse_pos)
            
            # Redraw overlay and message
            self.screen.blit(overlay, (0, 0))
            self.screen.blit(shadow_label, shadow_rect)
            self.screen.blit(label, msg_rect)
            
            # Draw buttons
            self.draw_button("Try Again", try_again_rect, GREEN, DARK_GREEN, try_again_hover)
            self.draw_button("Exit", exit_rect, RED, DARK_RED, exit_hover)
            
            pygame.display.update()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if try_again_rect.collidepoint(event.pos):
                        return 'try_again'
                    elif exit_rect.collidepoint(event.pos):
                        return 'exit'
        
        return 'exit'
