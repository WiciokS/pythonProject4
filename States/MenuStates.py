import pygame

from States.State import State, StateName


class PausedState(State):
    def __init__(self, state_context):
        super().__init__(StateName.PAUSE, state_context, root_state=True)

    def tick(self):
        super().tick()

        # Draw a black screen
        self.state_context.app_var.screen.fill((0, 0, 0))

        # On ESC, unpause the game
        for event in self.state_context.app_var.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    for state in self.state_context.persistent_states:
                        if state.state_name is StateName.GAMEPLAY:
                            self.switch_states(state)
                            break
                    Exception("No gameplay state found to unpause to.")

    def enter(self):
        pass

    def exit(self):
        pass
