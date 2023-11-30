from abc import ABC, abstractmethod
from enum import Enum


class StateName(Enum):
    MAIN_MENU = 0
    GAMEPLAY = 1
    UNPAUSED_GAMEPLAY = 10
    PAUSED_GAMEPLAY = 11


class State(ABC):
    def __init__(self, state_name):
        self.state_name = state_name
        pass
    @abstractmethod
    def tick(self):
        pass

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    def switch_states(self, state):
        self.exit()
        self.context.current_state = state
        self.context.current_state.enter()
