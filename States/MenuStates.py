import pygame
import os

from States.State import State, StateName, StateFactory
from UI.AnimatedButton import AnimatedButton
from UI.MapManager import MapManager


class PausedState(State):
    def __init__(self, state_context):

        # create a resume button using AnimatedButton class
        button_idle_path = "Sprites/Buttons/GenericButton/Frame1.png"
        button_press_path = "Sprites/Buttons/GenericButton/Frame2.png"
        self.button_resume = AnimatedButton(button_idle_path, button_press_path, "Resume", 50, 300, 100)
        # Set position of resume button to center  of screen and 200 pixels above center
        self.button_resume.rect.center = state_context.app_var.screen.get_rect().center
        self.button_resume.rect.centery -= 100

        # create a quit button using AnimatedButton class
        self.button_quit = AnimatedButton(button_idle_path, button_press_path, "Quit", 50, 300, 100)
        # Set position of quit button to center  of screen after resume button
        self.button_quit.rect.center = (self.button_resume.rect.centerx, self.button_resume.rect.centery + 300)

        # Create Back to menu Button
        self.button_back = AnimatedButton(button_idle_path, button_press_path,
                                          "Back to Menu", 50, 300, 100)
        # Set position of back button to center of screen before resume button
        self.button_back.rect.center = (self.button_resume.rect.centerx, self.button_resume.rect.centery + 150)

        # Create collision rects for the buttons
        self.button_resume_collision_rect = pygame.Rect(self.button_resume.rect)
        self.button_quit_collision_rect = pygame.Rect(self.button_quit.rect)
        self.button_back_collision_rect = pygame.Rect(self.button_back.rect)

        super().__init__(StateName.PAUSE, state_context, root_state=True)

    def tick(self):
        super().tick()

        # Draw a black screen
        self.state_context.app_var.screen.fill((128, 128, 128))

        # draw the button
        self.state_context.app_var.screen.blit(self.button_resume.image, self.button_resume.rect)
        self.state_context.app_var.screen.blit(self.button_quit.image, self.button_quit.rect)
        self.state_context.app_var.screen.blit(self.button_back.image, self.button_back.rect)

        # check if the button is pressed on collision
        for event in self.state_context.app_var.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_resume_collision_rect.collidepoint(pygame.mouse.get_pos()):
                    self.button_resume.turn_pressed()
                    break
                elif self.button_quit_collision_rect.collidepoint(pygame.mouse.get_pos()):
                    self.button_quit.turn_pressed()
                    break
                elif self.button_back_collision_rect.collidepoint(pygame.mouse.get_pos()):
                    self.button_back.turn_pressed()
                    break
            if event.type == pygame.MOUSEBUTTONUP:
                self.button_resume.turn_default()
                self.button_quit.turn_default()
                self.button_back.turn_default()
                if self.button_resume_collision_rect.collidepoint(pygame.mouse.get_pos()):
                    for state in self.state_context.persistent_states:
                        if state.state_name is StateName.GAMEPLAY:
                            self.switch_states(state)
                            break
                    Exception("No gameplay state found to unpause to.")
                elif self.button_quit_collision_rect.collidepoint(pygame.mouse.get_pos()):
                    self.state_context.app_var.app_running = False
                    break
                elif self.button_back_collision_rect.collidepoint(pygame.mouse.get_pos()):
                    self.switch_states(StateFactory.create_state(StateName.MAIN_MENU, self.state_context))
                    Exception("No main menu state found to go back to.")

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
        self.button_start.rect.center = (state_context.app_var.default_screen_size[0]//2, state_context.app_var.default_screen_size[1]//2)

        # create a quit button using AnimatedButton class
        self.button_quit = AnimatedButton(button_idle_path, button_press_path, "Quit", 50, 300, 100)
        self.button_quit.rect.center = (self.button_start.rect.centerx, self.button_start.rect.centery + 200)

        # Create collision rects for the buttons
        self.button_start_collision_rect = pygame.Rect(self.button_start.rect)
        self.button_quit_collision_rect = pygame.Rect(self.button_quit.rect)

        # Create Back Button
        self.button_back = AnimatedButton(button_idle_path, button_press_path,
                                          "Back", 50, 300, 100)
        # Set position of back button to left bottom corner
        self.button_back.rect.bottomleft = (40, 600)
        # Create collision rect for back button
        self.button_back_collision_rect = pygame.Rect(self.button_back.rect)

        self.default_screen_size = state_context.app_var.default_screen_size

        # Load maps with scaling
        self.map_manager = MapManager('Maps/Images', 'Levels',
                                      state_context.app_var.screen, scale_size=(300, 200))

        self.is_main_menu = True

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
        self.set_background_image("Sprites/Background/MainMenuBackground.png")
        # draw the button
        if self.is_main_menu:
            self.draw_button(self.button_start.image, self.button_start.rect)
            self.draw_button(self.button_quit.image, self.button_quit.rect)
        else:
            self.draw_button(self.button_back.image, self.button_back.rect)
            # On button back pressed, switch to main menu true

            for event in self.state_context.app_var.events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_back_collision_rect.collidepoint(pygame.mouse.get_pos()):
                        self.button_back.turn_pressed()
                        break
                if event.type == pygame.MOUSEBUTTONUP:
                    self.button_back.turn_default()
                    if self.button_back_collision_rect.collidepoint(pygame.mouse.get_pos()):
                        self.is_main_menu = True
                        break
            self.map_manager.draw_maps_in_row(40, 40)
            # check which map is pressed and use the map name to get the json file from self.level_files when start level
            for event in self.state_context.app_var.events:
                if event.type == pygame.MOUSEBUTTONUP:
                    for map in self.map_manager.get_maps():
                        if map['rect'].collidepoint(pygame.mouse.get_pos()):
                            # Get data from level files by name
                            for file in self.level_files:
                                if file == map['data']['map'] + ".json":
                                    self.state_context.game_var.build_level(file)
                                    self.switch_states(
                                        StateFactory.create_state(StateName.GAMEPLAY, self.state_context))
                            break

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
                    # self.switch_states(StateFactory.create_state(StateName.GAMEPLAY, self.state_context))
                    self.is_main_menu = False
                    break
                elif self.button_quit_collision_rect.collidepoint(pygame.mouse.get_pos()):
                    self.state_context.app_var.app_running = False
                    break

    def enter(self):
        for file in os.listdir("Levels"):
            if file.endswith(".json"):
                self.level_files.append(file)
        self.state_context.app_var.screen = pygame.display.set_mode(self.default_screen_size)

    def exit(self):
        pass
