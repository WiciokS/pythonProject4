import pygame
import os

from States.State import State, StateName, StateFactory


class PausedState(State):
    def __init__(self, state_context):
        super().__init__(StateName.PAUSE, state_context, root_state=True)

    def tick(self):
        super().tick()

        # Draw a black screen
        self.state_context.app_var.screen.fill((0, 0, 0))

        # On ESC, unpause the game
        for event in self.state_context.app_var.events:
            if event.type == pygame.KEYUP:
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


class MainMenuState(State):

    def __init__(self, state_context):
        self.levels = []
        super().__init__(StateName.MAIN_MENU, state_context, root_state=True)

    def tick(self):
        for event in self.state_context.app_var.events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.switch_states(StateFactory.create_state(StateName.GAMEPLAY, self.state_context))
                    break

    def enter(self):
        for file in os.listdir("Levels"):
            if file.endswith(".json"):
                self.levels.append(file)




    def exit(self):
        pass
