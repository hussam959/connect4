"""Game Controller - handles game flow and logic"""

import pygame
import math
from connect4_game import Connect4Game
from ai_player import AIPlayer
from game_ui import GameUI
from constants import *


class GameController:
    def __init__(self):
        self.ui = GameUI()
        self.game = None
        self.ai = None
        self.turn = 0
        self.game_over = False

    def reset_game(self):
        """Reset game state for new game"""
        self.game = Connect4Game()
        self.ai = AIPlayer(piece=PLAYER2_PIECE)
        self.turn = 0
        self.game_over = False
        self.ui.draw_board(self.game.board)

    def handle_player_move(self, col):
        """Handle player's move"""
        if self.game.is_valid_location(col):
            row = self.game.get_next_open_row(col)
            self.game.drop_piece(row, col, PLAYER1_PIECE)
            self.ui.draw_board(self.game.board)
            
            if self.game.winning_move(PLAYER1_PIECE):
                self.game_over = True
                return self.ui.show_game_over_screen("You Win! 🎉", RED)
            
            self.turn = 1
        return None

    def handle_ai_move(self):
        """Handle AI's move"""
        pygame.time.wait(AI_DELAY)
        col, score = self.ai.minimax(self.game, AI_DEPTH, -math.inf, math.inf, True)
        
        if col is not None and self.game.is_valid_location(col):
            row = self.game.get_next_open_row(col)
            self.game.drop_piece(row, col, PLAYER2_PIECE)
            self.ui.draw_board(self.game.board)
            
            if self.game.winning_move(PLAYER2_PIECE):
                self.game_over = True
                return self.ui.show_game_over_screen("AI Wins! 🤖", YELLOW)
            
            self.turn = 0
        return None

    def check_draw(self):
        """Check if game is a draw"""
        if (self.game.is_terminal_node() and 
            not self.game.winning_move(PLAYER1_PIECE) and 
            not self.game.winning_move(PLAYER2_PIECE)):
            self.game_over = True
            return self.ui.show_game_over_screen("It's a Draw! 🤝", LIGHT_GRAY)
        return None

    def run(self):
        """Main game loop"""
        self.reset_game()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                # Handle player move
                if (event.type == pygame.MOUSEBUTTONDOWN and 
                    self.turn == 0 and not self.game_over):
                    col = event.pos[0] // SQUARESIZE
                    result = self.handle_player_move(col)
                    
                    if result == 'try_again':
                        return True
                    elif result == 'exit':
                        return False
            
            # Handle AI move
            if self.turn == 1 and not self.game_over:
                result = self.handle_ai_move()
                
                if result == 'try_again':
                    return True
                elif result == 'exit':
                    return False
            
            # Check for draw
            if not self.game_over:
                result = self.check_draw()
                
                if result == 'try_again':
                    return True
                elif result == 'exit':
                    return False
        
        return False
