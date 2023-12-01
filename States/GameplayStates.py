import pygame

from States.State import State, StateName, StateFactory


class PrepareGameState(State):
    def __init__(self, context_state_manager):
        super().__init__(StateName.PREPARE_GAME, context_state_manager, root_state=False)

    def tick(self):
        # Make tower sprite follow mouse
        mouse_pos = pygame.mouse.get_pos()
        if self.state_context.game_var.selected_tower is not None:
            self.state_context.game_var.selected_tower.rect.center = mouse_pos
            self.state_context.game_var.selected_tower.draw(self.state_context.app_var.screen)

        # On left click, place tower
        for event in self.state_context.app_var.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.state_context.game_var.selected_tower is not None:
                        cell = self.state_context.game_var.level.map.convert_screen_coordinates_to_cells(mouse_pos)[0]
                        if cell is not None and cell.tower is None:
                            self.state_context.game_var.level.deployed_towers.append(
                                self.state_context.game_var.selected_tower)
                            self.state_context.game_var.selected_tower.place(cell)
                            self.state_context.game_var.selected_tower = None

    def enter(self):
        self.state_context.game_var.selected_tower = (
            self.state_context.game_var.level.available_towers[0]())

    def exit(self):
        pass


class ActiveGameState(State):
    def __init__(self, context_state_manager):
        super().__init__(StateName.ACTIVE_GAME, context_state_manager, root_state=False)

    def tick(self):
        self.state_context.level.tick()

    def enter(self):
        pass

    def exit(self):
        pass


class GameplayState(State):
    def __init__(self, context_state_manager):
        super().__init__(StateName.GAMEPLAY, context_state_manager, root_state=True)

    def tick(self):
        # On ESC, pause the game
        for event in self.state_context.app_var.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.switch_states(StateFactory.create_state(StateName.PAUSE, self.state_context))

        # Draw map
        self.state_context.game_var.level.map.draw(self.state_context.app_var.screen)

        # Show time_ms in bottom left corner
        time_ms_text = (pygame.font.SysFont("Arial", 20)
                        .render(str(self.state_context.game_var.level.time_ms), True, (0, 0, 0)))

        self.state_context.app_var.screen.blit(
            time_ms_text, (0, self.state_context.app_var.screen.get_height() - time_ms_text.get_height()))

        # Draw the towers and the enemies
        for tower in self.state_context.game_var.level.deployed_towers:
            tower.draw(self.state_context.app_var.screen)

        for enemy in self.state_context.game_var.level.deployed_enemies:
            # Move the enemy if it's not at the end of the path
            if not enemy.at_end_of_path():
                enemy.move()
                enemy.draw(self.state_context.app_var.screen)
            else:
                self.state_context.game_var.level.deployed_enemies.remove(enemy)
                enemy.kill()

        super().tick()

    def enter(self):
        if self not in self.state_context.persistent_states:
            self.state_context.persistent_states.append(self)
            self.switch_substate(StateFactory.create_state(StateName.PREPARE_GAME, self.state_context))
            self.state_context.persistent_states.append(self.substate)

    def exit(self):
        pass
