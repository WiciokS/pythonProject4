import pygame

from Area.AreaInput import AreaInput, AreaName


class MenuAreaInput(AreaInput):

    def tick(self):
        pass

    def __init__(self, state_context, top_left_x=0, top_left_y=0, width=0, height=0):
        super().__init__(state_context, AreaName.MENU, top_left_x, top_left_y, width, height)
        #Load sprites images
        self.archer_icon = pygame.image.load('Sprites/Archer/ArcherDefault.png')
        self.mage_icon = pygame.image.load('Sprites/Mage/MageDefault.png')
        self.elemental_icon = pygame.image.load('Sprites/WaterElemental/WaterElementalDefault.png')

    def process_mouse_input_event(self, event):
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        print(f"Mouse Position: {mouse_pos}")  # Debugging output

        # Define rectangles for each icon
        mage_rect = pygame.Rect(self.top_left_x + 48, self.top_left_y + 64, self.mage_icon.get_width(),
                                self.mage_icon.get_height())
        print(f"Mage Rect: {mage_rect}")  # Debugging output
        archer_rect = pygame.Rect(self.top_left_x + 48, self.top_left_y + 128, self.archer_icon.get_width(),
                                  self.archer_icon.get_height())
        print(f"Archer Rect: {archer_rect}")  # Debugging output
        elemental_rect = pygame.Rect(self.top_left_x + 48, self.top_left_y + 192, self.elemental_icon.get_width(),
                                     self.elemental_icon.get_height())
        print(f"Elemental Rect: {elemental_rect}")  # Debugging output

        # Check if mouse is over any icon
        if mage_rect.collidepoint(mouse_pos):
            print("Mage clicked")  # Debugging output
            self.state_context.game_var.selected_tower = self.state_context.game_var.level.available_towers[0](
                self.state_context)
        elif archer_rect.collidepoint(mouse_pos):
            print("Archer clicked")  # Debugging output
            self.state_context.game_var.selected_tower = self.state_context.game_var.level.available_towers[1](
                self.state_context)
        elif elemental_rect.collidepoint(mouse_pos):
            print("Elemental clicked")  # Debugging output
            self.state_context.game_var.selected_tower = self.state_context.game_var.level.available_towers[2](
                self.state_context)

    def draw(self, screen):
        # Draw background from top_left_x top_left_y to bottom_right_x bottom_right_y
        screen.fill((128, 128, 128), (self.top_left_x, self.top_left_y, self.bottom_right_x, self.bottom_right_y))
        # Draw icons
        screen.blit(self.mage_icon, (self.top_left_x + 48, self.top_left_y + 64))
        screen.blit(self.archer_icon, (self.top_left_x + 48, self.top_left_y + 128))
        screen.blit(self.elemental_icon, (self.top_left_x + 48, self.top_left_y + 192))
