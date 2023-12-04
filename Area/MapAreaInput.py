import pygame

from Area.AreaInput import AreaInput, AreaName
from States.State import StateName


class MapAreaInput(AreaInput):

    def __init__(self, state_context, top_left_x=0, top_left_y=0, width=0, height=0):
        super().__init__(state_context, AreaName.MAP, top_left_x, top_left_y, width, height)

    def tick(self):
        mouse_pos = pygame.mouse.get_pos()
        # Make tower sprite follow mouse
        if (self.state_context.game_var.selected_tower is not None and
                self.state_context.game_var.selected_tower.cell is None):
            self.state_context.game_var.selected_tower.rect.center = mouse_pos
            self.state_context.game_var.selected_tower.draw(self.state_context.app_var.screen)

    def alternative_tick(self):
        pass

    def process_mouse_input_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.button == 1:  # Left click
            # Place tower (PREPARE_GAME)
            if self.state_context.game_var.selected_tower is not None:  # If a tower is selected
                cell = self.state_context.game_var.level.map.convert_screen_coordinates_to_cells(mouse_pos)[0]
                if cell is not None:  # If the mouse is inside the map
                    if cell.tower is not None:  # If the selected tower is the same as the clicked tower
                        # if the selected tower is the same as the clicked tower
                        if self.state_context.game_var.selected_tower is cell.tower:
                            # Pickup the tower if substate is PREPARE_GAME
                            if self.state_context.current_state_root.substate.state_name is StateName.PREPARE_GAME:
                                cell.tower.pickup()
                                self.state_context.game_var.level.deployed_towers.remove(
                                    self.state_context.game_var.selected_tower)
                            return
                    # if the cell tower is empty
                    if cell.tower is None:
                        # If the selected tower is not placed
                        if self.state_context.game_var.selected_tower.cell is None:
                            if cell.buildable:  # If the cell is buildable, place the tower
                                self.state_context.game_var.selected_tower.place(cell)
                                if cell.tower is self.state_context.game_var.selected_tower:
                                    self.state_context.game_var.level.deployed_towers.append(
                                        self.state_context.game_var.selected_tower)
                                self.state_context.game_var.selected_tower = None
                                return
                        else:
                            self.state_context.game_var.selected_tower = None
                            return

            # Select tower
            if self.state_context.game_var.selected_tower is None:
                cell = self.state_context.game_var.level.map.convert_screen_coordinates_to_cells(mouse_pos)[0]
                if cell is not None:  # If the mouse is inside the map
                    if cell.tower is not None:  # If the tower on cell is not empty
                        # If the selected tower is not the same as the clicked tower, select the clicked tower
                        if self.state_context.game_var.selected_tower is not cell.tower:
                            self.state_context.game_var.selected_tower = cell.tower
                            return

        if event.button == 3:  # Right click
            # Clear selection
            if self.state_context.game_var.selected_tower is not None:  # If a tower is selected
                if self.state_context.game_var.selected_tower.cell is None:  # If the selected tower is not placed
                    if self.state_context.game_var.selected_tower.last_cell is not None:
                        self.state_context.game_var.selected_tower.place(
                            self.state_context.game_var.selected_tower.last_cell)
                        self.state_context.game_var.selected_tower.attach(
                            self.state_context.game_var.selected_tower.last_cell)
                        self.state_context.game_var.selected_tower = None
                        return
                    else:
                        self.state_context.game_var.selected_tower.remove()
                        self.state_context.game_var.selected_tower = None
                else:
                    self.state_context.game_var.selected_tower = None
                    return

    def draw(self, screen):
        pass
