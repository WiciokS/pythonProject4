import pygame

from States.State import StateName
from States.StateContext import StateContext


class GameManager:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        pygame.display.set_caption("Tower Defence")

        self.state_context = StateContext(StateName.MAIN_MENU)

    def run(self):
        # Game loop
        self.state_context.app_var.app_running = True
        while self.state_context.app_var.app_running:
            # Tick the current state
            self.state_context.tick()

            # Update the display
            pygame.display.update()

        # Quit Pygame
        pygame.quit()
