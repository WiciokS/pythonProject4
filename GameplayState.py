import pygame

from Enemy import Enemy
from GameManager import GameStatus
from Maps.TestMap import TestMap
from Tower import Tower
from State import State, StateName


class PausedGameplayState(State):
    def __init__(self, context):
        super().__init__(StateName.PAUSED_GAMEPLAY, context)

    def tick(self):
        GameStatus.screen.fill((0, 0, 0))
        # On ESC, unpause the game
        for event in GameStatus.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.switch_states(self.context.persistent_state)

    def enter(self):
        pass

    def exit(self):
        pass


class UnpausedGameplayState(State):
    def __init__(self, context):
        super().__init__(StateName.UNPAUSED_GAMEPLAY, context)
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
                    self.context.persistent_state = self
                    self.switch_states(PausedGameplayState(self.context))

        # Increase time
        self.context.time_ms += GameStatus.clock.get_time()

        # Draw map
        self.game_map.draw(GameStatus.screen)

        # Draw the towers and the enemies
        for tower in self.towers:
            tower.draw(GameStatus.screen)
        for enemy in self.enemies:
            # Move the enemy if it's not at the end of the path
            if not enemy.at_end_of_path():
                enemy.move()
            enemy.draw(GameStatus.screen)

    def enter(self):
        GameStatus.fps = 144

    def exit(self):
        pass


class GameplayState(State):
    def __init__(self, context):
        super().__init__(StateName.GAMEPLAY, context)
        from StateManager import StateManager  # This import is here to avoid a circular import
        self.substate_manager = StateManager(StateName.UNPAUSED_GAMEPLAY)
        self.substate_manager.persistent_state = UnpausedGameplayState(context)
        self.substate_manager.current_state.enter()

    def tick(self):
        # Tick the current substate
        self.substate_manager.tick()
        # On ESC, pause the game
        for event in GameStatus.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.substate_manager.current_state.state_name == StateName.PAUSED_GAMEPLAY:
                        self.substate_manager.switch_states(self.unpaused_state_persistence)
                    else:
                        self.substate_manager.switch_states(PausedGameplayState())

    def enter(self):
        pass

    def exit(self):
        pass
