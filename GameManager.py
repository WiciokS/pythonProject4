import pygame
import sys
from GameplayState import GameplayState
from StateManager import StateManager


class GameManager:
    def __init__(self):
        self.state_manager = StateManager(GameplayState())
        # Initialize Pygame
        pygame.init()

        # Set up the display
        screen = pygame.display.set_mode((800, 600))

        # Create a clock object to control the frame rate
        clock = pygame.time.Clock()

        # Create a tower and an enemy for demonstration

        # Game loop
        running = True
        while running:
            # Ensure the program maintains a rate of 30 frames per second
            clock.tick(144)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update the display
            pygame.display.update()

        # Quit Pygame
        pygame.quit()


