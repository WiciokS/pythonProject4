import pygame

from GameplayState import GameplayState, PausedState
from State import StateName


class StateFactory:
    @staticmethod
    def create_state(state_name, context_state_manager):
        if state_name == StateName.GAMEPLAY:
            return GameplayState(context_state_manager)
        elif state_name == StateName.PAUSE:
            return PausedState(context_state_manager)
        else:
            raise ValueError("Invalid state name")


class StateManager:
    def __init__(self, state_name):
        self.time_ms = 0
        self.app_running = False
        self.clock = pygame.time.Clock()
        self.fps = 144
        self.screen = pygame.display.set_mode((800, 600))
        self.events = None
        self.current_state = StateFactory.create_state(state_name, self)
        self.persistent_state = None
        self.current_state.enter()

    def tick(self):
        self.clock.tick(self.fps)
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.app_running = False
        self.current_state.tick()
