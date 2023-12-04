import pygame
import os

from States.State import State, StateName, StateFactory
from UI.AnimatedButton import AnimatedButton
from UI.MapManager import MapManager


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

        button_idle_path = "Sprites/Buttons/GenericButton/Frame1.png"
        button_press_path = "Sprites/Buttons/GenericButton/Frame2.png"
        # create a start button using AnimatedButton class
        self.button_start = AnimatedButton(button_idle_path, button_press_path, "Start", 50, 300, 100)
        self.button_start.rect.center = (640, 320)

        # create a quit button using AnimatedButton class
        self.button_quit = AnimatedButton(button_idle_path, button_press_path, "Quit", 50, 300, 100)
        self.button_quit.rect.center = (640, 520)

        # Create collision rects for the buttons
        self.button_start_collision_rect = pygame.Rect(self.button_start.rect)
        self.button_quit_collision_rect = pygame.Rect(self.button_quit.rect)

        self.map_manager = MapManager()

        # Load maps
        self.map_manager.load_map('Maps/TestMap.png', 'Levels/Test.json', scale_size=(200, 150))
        self.map_manager.load_map('Maps/BlueMagicMap.png', 'Levels/BlueMagicMap.json', scale_size=(200, 150))


        super().__init__(StateName.MAIN_MENU, state_context, root_state=True)


    def set_background_image(self, image):
        # Draw a grey screen
        self.state_context.app_var.screen.fill((128, 128, 128))
        # Draw background image
        background_image = pygame.image.load(image)
        background_image = pygame.transform.scale(background_image, (1280, 640))
        self.state_context.app_var.screen.blit(background_image, (0, 0))

    # create draw function
    def draw_button(self, image, rect):
        self.state_context.app_var.screen.blit(image, rect)

    def tick(self):
        # Set background image
        self.set_background_image("Sprites/Background/Fon.png")
        # draw the button
        self.draw_button(self.button_start.image, self.button_start.rect)
        self.draw_button(self.button_quit.image, self.button_quit.rect)

        # Draw the maps using function
        self.map_manager.draw_maps_in_row(self.state_context.app_var.screen, 40, 40, 40)

        # check if the button is pressed on collision
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
