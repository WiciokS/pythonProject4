import pygame

from States.State import StateName
from States.StateManager import StateManager


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
        self.state_manager.app_running = True
        while self.state_manager.app_running:
            # Tick the current state
            self.state_manager.tick()

            # Update the display
            pygame.display.update()

        # Quit Pygame
        pygame.quit()
