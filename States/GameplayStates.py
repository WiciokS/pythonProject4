import pygame

from Area.MapAreaInput import MapAreaInput
from Area.MenuAreaInput import MenuAreaInput
from States.State import State, StateName, StateFactory


class PrepareGameState(State):
    def __init__(self, state_context):
        super().__init__(StateName.PREPARE_GAME, state_context, root_state=False)

    def tick(self):
        for event in self.state_context.app_var.events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.switch_states(StateFactory.create_state(StateName.ACTIVE_GAME, self.state_context))

    def enter(self):
        pass

    def exit(self):
        pass


class ActiveGameState(State):
    def __init__(self, state_context):
        super().__init__(StateName.ACTIVE_GAME, state_context, root_state=False)

    def tick(self):
        self.state_context.game_var.level.tick()
        for tower in self.state_context.game_var.level.deployed_towers:
            tower.tick()

    def enter(self):
        pass

    def exit(self):
        pass


class GameplayState(State):
    def __init__(self, state_context):
        super().__init__(StateName.GAMEPLAY, state_context, root_state=True)

    def tick(self):

        mouse_pos = pygame.mouse.get_pos()

        # Draw map
        self.state_context.game_var.level.map.draw(self.state_context.app_var.screen)

        # If a tower is selected, draw its range and possible build cells
        if self.state_context.game_var.selected_tower is not None:
            # Draw cell outlines
            if self.state_context.game_var.selected_tower.cell is None:
                for cell in self.state_context.game_var.level.map.cells:
                    cell.draw(self.state_context.app_var.screen)
            else:
                self.state_context.game_var.selected_tower.cell.draw(self.state_context.app_var.screen)

        # Show time_ms in bottom left corner
        time_ms_text = (pygame.font.SysFont("Arial", 20)
                        .render(str(self.state_context.game_var.level.time_ms), True, (0, 0, 0)))

        self.state_context.app_var.screen.blit(
            time_ms_text, (0, self.state_context.app_var.screen.get_height() - time_ms_text.get_height()))

        if self.state_context.game_var.selected_tower is not None:
            self.state_context.game_var.selected_tower.draw_range(self.state_context.app_var.screen)

        # Draw the towers and the enemies
        for tower in self.state_context.game_var.level.deployed_towers:
            tower.draw(self.state_context.app_var.screen)

        for enemy in self.state_context.game_var.level.deployed_enemies:
            # Orc the enemy if it's not at the end of the path
            if not enemy.at_end_of_path():
                enemy.tick()
                if enemy is None:
                    continue
                enemy.draw(self.state_context.app_var.screen)
            else:
                enemy.remove()

        for projectile in self.state_context.game_var.level.projectiles:
            projectile.tick()
            if projectile is None:
                continue
            projectile.draw(self.state_context.app_var.screen)

        for event in self.state_context.app_var.events:
            if event.type == pygame.KEYUP:
                # On ESC, pause the game
                if event.key == pygame.K_ESCAPE:
                    self.switch_states(StateFactory.create_state(StateName.PAUSE, self.state_context))
                    break
            if event.type == pygame.MOUSEBUTTONUP:
                for area in self.state_context.game_var.input_areas:
                    if area.inside(mouse_pos):
                        area.process_mouse_input_event(event)
                        break

        for area in self.state_context.game_var.input_areas:
            if area.inside(mouse_pos):
                area.tick()
            area.draw(self.state_context.app_var.screen)

        super().tick()

    def enter(self):
        if self not in self.state_context.persistent_states:
            self.state_context.persistent_states.append(self)
            self.switch_substate(StateFactory.create_state(StateName.PREPARE_GAME, self.state_context))
            self.state_context.persistent_states.append(self.substate)
            self.state_context.app_var.screen = pygame.display.set_mode(
                (self.state_context.game_var.level.map.width + 128,
                 self.state_context.game_var.level.map.height))
            map_area = MapAreaInput(self.state_context,
                                    top_left_x=0,
                                    top_left_y=0,
                                    width=self.state_context.game_var.level.map.width,
                                    height=self.state_context.game_var.level.map.height)
            self.state_context.game_var.input_areas.append(map_area)
            buy_area = MenuAreaInput(self.state_context,
                                     top_left_x=self.state_context.game_var.level.map.width,
                                     top_left_y=0,
                                     width=self.state_context.app_var.screen.get_width(),
                                     height=self.state_context.app_var.screen.get_height())
            self.state_context.game_var.input_areas.append(buy_area)

    def exit(self):
        pass
