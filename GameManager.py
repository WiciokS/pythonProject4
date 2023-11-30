import pygame

from State import StateName
from StateManager import StateManager


class GameManager:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        pygame.display.set_caption("Tower Defence")

        # Set up the state manager (GAMEPLAY is TEMPORARY, MAIN_MENU SHOULD BE FIRST)
        self.state_manager = StateManager(StateName.GAMEPLAY)

    def run(self):
        # Game loop
        running = True
        while running:
            GameStatus.clock.tick(GameStatus.fps)

            GameStatus.events = pygame.event.get()

            for event in GameStatus.events:
                if event.type == pygame.QUIT:
                    running = False

            # Tick the current state
            self.state_manager.tick()

            # Update the display
            pygame.display.update()

        # Quit Pygame
        pygame.quit()
