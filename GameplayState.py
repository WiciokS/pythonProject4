import pygame

from Enemy import Enemy
from Maps.TestMap import TestMap
from Tower import Tower
from State import State, StateName


class PausedState(State):
    def __init__(self, context_state_manager):
        super().__init__(StateName.PAUSE, context_state_manager, root_state=True)

    def tick(self):
        super().tick()

        # Draw a black screen
        self.context_state_manager.screen.fill((0, 0, 0))

        # On ESC, unpause the game
        for event in self.context_state_manager.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.switch_states(self.context_state_manager.persistent_state)

    def enter(self):
        pass

    def exit(self):
        pass


class GameplayState(State):
    def __init__(self, context_state_manager):
        super().__init__(StateName.GAMEPLAY, context_state_manager, root_state=True)

        # Set the persistent state to gameplay
        self.context_state_manager.persistent_state = self

        # Game Related
        self.towers = []
        self.enemies = []

        # TEMPORARY
        self.game_map = TestMap()
        self.towers.append(Tower(self.game_map.get_cell(3, 4)))
        self.enemies.append(Enemy(self.game_map.get_path()))

    def tick(self):
        super().tick()

        # On ESC, pause the game
        for event in self.context_state_manager.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.context_state_manager.persistent_state = self
                    from StateManager import StateFactory  # Avoid circular import
                    self.switch_states(StateFactory.create_state(StateName.PAUSE, self.context_state_manager))

        # Increase time
        self.context_state_manager.time_ms += self.context_state_manager.clock.get_time()

        # Draw map
        self.game_map.draw(self.context_state_manager.screen)

        # Show time_ms in bottom left corner
        time_ms_text = (pygame.font.SysFont("Arial", 20)
                        .render(str(self.context_state_manager.time_ms), True, (0, 0, 0)))

        self.context_state_manager.screen.blit(
            time_ms_text, (0, self.context_state_manager.screen.get_height() - time_ms_text.get_height()))

        # Draw the towers and the enemies
        for tower in self.towers:
            tower.draw(self.context_state_manager.screen)

        for enemy in self.enemies:
            # Move the enemy if it's not at the end of the path
            if not enemy.at_end_of_path():
                enemy.move()
            enemy.draw(self.context_state_manager.screen)

    def enter(self):
        pass

    def exit(self):
        pass
