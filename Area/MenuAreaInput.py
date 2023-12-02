import pygame
from Area.AreaInput import AreaInput, AreaName


class MenuAreaInput(AreaInput):

    def tick(self):
        pass

    def __init__(self, state_context, top_left_x=0, top_left_y=0, width=0, height=0):
        super().__init__(state_context, AreaName.MENU, top_left_x, top_left_y, width, height)
        self.tower_icons = []
        self.gold_cost_texts = []
        self.icon_collision_rects = []
        y_offset = 64  # Starting y position for the first icon

        for index, tower_class in enumerate(state_context.game_var.level.available_towers):
            # Dynamically load the icon based on the tower's class attribute
            icon_path = tower_class.icon_path
            icon_sprite = pygame.image.load(icon_path)
            self.tower_icons.append(icon_sprite)

            # Create a rectangle for collision detection
            rect = pygame.Rect(self.top_left_x + 48, self.top_left_y + y_offset, icon_sprite.get_width(),
                               icon_sprite.get_height())
            self.icon_collision_rects.append((rect, index))  # Append a tuple with the rect and index

            # Put text of gold cost below the icon
            gold_cost_text = pygame.font.SysFont("Arial", 20).render(
                str(tower_class.cost), True, (0, 0, 0))
            self.gold_cost_texts.append(gold_cost_text)

            # Increment y_offset for the next icon
            y_offset += icon_sprite.get_height() + 64

    def process_mouse_input_event(self, event):
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check each icon for a collision with the mouse click
        for rect, tower_index in self.icon_collision_rects:  # Corrected iteration
            if rect.collidepoint(mouse_pos):
                print(f"Icon {tower_index} clicked")  # Debugging output
                # Create the selected tower based on the clicked icon
                if (self.state_context.game_var.level.gold >=
                        self.state_context.game_var.level.available_towers[tower_index].cost):
                    self.state_context.game_var.selected_tower = self.state_context.game_var.level.available_towers[
                        tower_index](self.state_context)
                break  # Exit the loop once a collision is found

    def draw(self, screen):
        # Draw background
        screen.fill((128, 128, 128), (self.top_left_x, self.top_left_y, self.bottom_right_x, self.bottom_right_y))

        screen.blit(pygame.font.SysFont("Arial", 20).
                    render(str(self.state_context.game_var.level.gold), True, (0, 0, 0)),
                    (self.top_left_x + 16, self.top_left_y + 16))

        # Draw tower icons
        for icon_sprite, (rect, _) in zip(self.tower_icons, self.icon_collision_rects):  # Corrected unpacking
            screen.blit(icon_sprite, rect.topleft)  # 'rect' must be a pygame.Rect object
            screen.blit(self.gold_cost_texts[self.icon_collision_rects.index((rect, _))],
                        (rect.centerx, rect.bottom + 8))
