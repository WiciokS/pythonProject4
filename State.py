from abc import ABC, abstractmethod
from enum import Enum


class StateName(Enum):
    MAIN_MENU = 0
    GAMEPLAY = 1
    PAUSE = 2


class State(ABC):
    def __init__(self, state_name, context_state_manager):
        self.state_name = state_name
        self.context_state_manager = context_state_manager
        self.substates = []
        self.parent_states = []
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
        self.context_state_manager.current_state = state
        self.context_state_manager.current_state.enter()
