"""Main entry point - only handles initialization and game loop"""

import pygame
import sys
from game_controller import GameController


def main():
    """Initialize pygame and start game"""
    pygame.init()
    
    controller = GameController()
    
    # Game loop - continue if player chooses "Try Again"
    while controller.run():
        controller.reset_game()
    
    # Cleanup
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
