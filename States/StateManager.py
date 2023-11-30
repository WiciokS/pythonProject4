import pygame

from Enemies.Orc import Orc
from States.GameplayStates import GameplayState, ActiveGameState, BuildGameState
from Level import LevelBuilder
from States.MenuStates import PausedState
from States.State import StateName
from Towers.Mage import Mage


class StateFactory:
    @staticmethod
    def create_state(state_name, context_state_manager):
        if state_name == StateName.GAMEPLAY:
            return GameplayState(context_state_manager)
        elif state_name == StateName.PAUSE:
            return PausedState(context_state_manager)
        elif state_name == StateName.ACTIVE_GAME:
            return ActiveGameState(context_state_manager)
        elif state_name == StateName.BUILD_GAME:
            return BuildGameState(context_state_manager)
        else:
            raise ValueError("Invalid state name")


class StateManager:
    def __init__(self, state_name):
        self.app_clock = pygame.time.Clock()
        self.app_running = False
        self.fps = 60
        self.screen = pygame.display.set_mode((960, 640))
        self.events = None
        self.current_state = StateFactory.create_state(state_name, self)
        self.persistent_state = None
        self.level = None
        self.selected_tower = None

        # TEMPORARY
        level_builder = LevelBuilder(pygame.time.Clock())
        level_builder.add_map("TestMap")
        level_builder.add_available_enemy(Orc)
        level_builder.add_available_tower(Mage)
        self.level = level_builder.build()

        self.current_state.enter()

    def tick(self):
        self.app_clock.tick(self.fps)
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.app_running = False
        self.current_state.tick()
