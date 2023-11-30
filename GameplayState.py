import pygame

from Enemy import Enemy
from GameManager import GameStatus
from Maps.TestMap import TestMap
from Tower import Tower
from State import State, StateName


class PausedGameplayState(State):
    def __init__(self, context_state_manager):
        super().__init__(StateName.PAUSED_GAMEPLAY, context_state_manager)

    def tick(self):
        GameStatus.screen.fill((0, 0, 0))
        # On ESC, unpause the game
        for event in GameStatus.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.switch_states(self.context_state_manager.persistent_state)

    def enter(self):
        pass

    def exit(self):
        pass


class UnpausedGameplayState(State):
    def __init__(self, context_state_manager):
        super().__init__(StateName.UNPAUSED_GAMEPLAY, context_state_manager)
        self.towers = []
        self.enemies = []

        # TEMPORARY
        self.game_map = TestMap()
        self.towers.append(Tower(self.game_map.get_cell(3, 4)))
        self.enemies.append(Enemy(self.game_map.get_path()))

    def tick(self):
        # On ESC, pause the game
        for event in GameStatus.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.context_state_manager.persistent_state = self
                    self.switch_states(PausedGameplayState(self.context_state_manager))

        # Increase time
        self.context_state_manager.time_ms += GameStatus.clock.get_time()

        # Draw map
        self.game_map.draw(GameStatus.screen)

        # Show time_ms in bottom left corner
        time_ms_text = pygame.font.SysFont("Arial", 20).render(str(self.context_state_manager.time_ms), True, (0, 0, 0))
        GameStatus.screen.blit(time_ms_text, (0, GameStatus.screen.get_height() - time_ms_text.get_height()))

        # Draw the towers and the enemies
        for tower in self.towers:
            tower.draw(GameStatus.screen)
        for enemy in self.enemies:
            # Move the enemy if it's not at the end of the path
            if not enemy.at_end_of_path():
                enemy.move()
            enemy.draw(GameStatus.screen)

    def enter(self):
        pass

    def exit(self):
        pass


class GameplayState(State):
    def __init__(self, context_state_manager):
        super().__init__(StateName.GAMEPLAY, context_state_manager)
        from StateManager import StateManager  # This import is here to avoid a circular import
        self.substate_manager = StateManager(StateName.UNPAUSED_GAMEPLAY)
        self.substate_manager.persistent_state = self.substate_manager.current_state
        self.substate_manager.current_state.enter()

    def tick(self):
        # Tick the current substate
        self.substate_manager.tick()

    def enter(self):
        pass

    def exit(self):
        pass
