import pygame
import os

from States.State import State, StateName, StateFactory
from UI.AnimatedButton import AnimatedButton


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
        self.level_files = []

        # create a start button using AnimatedButton class
        self.button_start = AnimatedButton("Sprites/Buttons/GenericButton/Frame1.png",
                                           "Sprites/Buttons/GenericButton/Frame2.png",
                                           "Start", 50, 300, 100)
        self.button_start.rect.center = (640, 320)

        # create a quit button using AnimatedButton class
        self.button_quit = AnimatedButton("Sprites/Buttons/GenericButton/Frame1.png",
                                          "Sprites/Buttons/GenericButton/Frame2.png",
                                          "Quit", 50, 300, 100)
        self.button_quit.rect.center = (640, 520)

        # Create collision rects for the buttons
        self.button_start_collision_rect = pygame.Rect(self.button_start.rect)
        self.button_quit_collision_rect = pygame.Rect(self.button_quit.rect)

        self.background_image = pygame.image.load("Sprites/Background/MainMenuBackground.png")
        self.background_image = pygame.transform.scale(self.background_image, (1280, 640))

        super().__init__(StateName.MAIN_MENU, state_context, root_state=True)

    def tick(self):
        # Draw background image
        self.state_context.app_var.screen.blit(self.background_image, (0, 0))
        # Draw the buttons
        self.state_context.app_var.screen.blit(self.button_start.image, self.button_start.rect)
        self.state_context.app_var.screen.blit(self.button_quit.image, self.button_quit.rect)

        # Check if the button is pressed on collision
        for event in self.state_context.app_var.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_start_collision_rect.collidepoint(pygame.mouse.get_pos()):
                    self.button_start.turn_pressed()
                    break
                elif self.button_quit_collision_rect.collidepoint(pygame.mouse.get_pos()):
                    self.button_quit.turn_pressed()
                    break
            if event.type == pygame.MOUSEBUTTONUP:
                self.button_start.turn_default()
                self.button_quit.turn_default()
                if self.button_start_collision_rect.collidepoint(pygame.mouse.get_pos()):
                    self.switch_states(StateFactory.create_state(StateName.GAMEPLAY, self.state_context))
                    break
                elif self.button_quit_collision_rect.collidepoint(pygame.mouse.get_pos()):
                    self.state_context.app_var.app_running = False
                    break

    def enter(self):
        for file in os.listdir("Levels"):
            if file.endswith(".json"):
                self.level_files.append(file)

    def exit(self):
        pass
