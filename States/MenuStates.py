import pygame

from States.State import State, StateName


class PausedState(State):
    def __init__(self, context_state_manager):
        super().__init__(StateName.PAUSE, context_state_manager, root_state=True)

    def tick(self):
        super().tick()

        # Draw a black screen
        self.context_state_manager.screen.fill((0, 0, 0))

        # On ESC, unpause the game
        for event in self.context_state_manager.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.switch_states(self.context_state_manager.persistent_state)

    def enter(self):
        pass

    def exit(self):
        pass