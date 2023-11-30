import pygame

from States.State import State, StateName


class BuildGameState(State):
    def __init__(self, context_state_manager):
        super().__init__(StateName.BUILD_GAME, context_state_manager, root_state=False)

    def tick(self):
        # Make tower sprite follow mouse
        mouse_pos = pygame.mouse.get_pos()
        if self.context_state_manager.selected_tower is not None:
            self.context_state_manager.selected_tower.rect.center = mouse_pos
            self.context_state_manager.selected_tower.draw(self.context_state_manager.screen)

        # On left click, place tower
        for event in self.context_state_manager.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cell = self.context_state_manager.level.map.convert_screen_coordinates_to_cells(mouse_pos)[0]
                    if cell is not None and cell.tower is None:
                        self.context_state_manager.level.deployed_towers.append(
                            self.context_state_manager.selected_tower)
                        self.context_state_manager.selected_tower.place(cell)
                        self.context_state_manager.selected_tower = None

    def enter(self):
        self.context_state_manager.selected_tower = self.context_state_manager.level.available_towers[0]()

    def exit(self):
        pass


class ActiveGameState(State):
    def __init__(self, context_state_manager):
        super().__init__(StateName.ACTIVE_GAME, context_state_manager, root_state=False)

    def tick(self):
        self.context_state_manager.level.tick()

    def enter(self):
        pass

    def exit(self):
        pass


class GameplayState(State):
    def __init__(self, context_state_manager):
        super().__init__(StateName.GAMEPLAY, context_state_manager, root_state=True)

    def tick(self):
        # On ESC, pause the game
        for event in self.context_state_manager.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.context_state_manager.persistent_state.state_name is StateName.ACTIVE_GAME:
                        self.context_state_manager.persistent_state = self.context_state_manager.persistent_state
                        from StateManager import StateFactory  # Avoid circular import
                        self.switch_states(StateFactory.create_state(StateName.PAUSE, self.context_state_manager))

        # Draw map
        self.context_state_manager.level.map.draw(self.context_state_manager.screen)

        # Show time_ms in bottom left corner
        time_ms_text = (pygame.font.SysFont("Arial", 20)
                        .render(str(self.context_state_manager.level.time_ms), True, (0, 0, 0)))

        self.context_state_manager.screen.blit(
            time_ms_text, (0, self.context_state_manager.screen.get_height() - time_ms_text.get_height()))

        # Draw the towers and the enemies
        for tower in self.context_state_manager.level.deployed_towers:
            tower.draw(self.context_state_manager.screen)

        for enemy in self.context_state_manager.level.deployed_enemies:
            # Move the enemy if it's not at the end of the path
            if not enemy.at_end_of_path():
                enemy.move()
                enemy.draw(self.context_state_manager.screen)
            else:
                self.context_state_manager.level.deployed_enemies.remove(enemy)
                enemy.kill()

        super().tick()

    def enter(self):
        if (self.context_state_manager.persistent_state is None
                or self.context_state_manager.persistent_state.state_name is not StateName.ACTIVE_GAME):
            from States.StateManager import StateFactory  # Avoid circular import
            self.context_state_manager.persistent_state = StateFactory.create_state(StateName.ACTIVE_GAME,
                                                                                    self.context_state_manager)
            self.switch_substate(StateFactory.create_state(StateName.BUILD_GAME, self.context_state_manager))

    def exit(self):
        pass
