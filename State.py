from abc import ABC, abstractmethod
from enum import Enum


class StateName(Enum):
    MAIN_MENU = 0
    GAMEPLAY = 1
    PAUSE = 2


class State(ABC):
    def __init__(self, state_name, context_state_manager, root_state=True):
        self.root_state = root_state
        self.state_name = state_name
        self.context_state_manager = context_state_manager
        self.substate = None
        self.parent_state = None
        pass

    @abstractmethod
    def tick(self):
        if self.substate is not None:
            self.substate.tick()

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    def switch_states(self, state):
        self.exit()
        if self.root_state:
            self.context_state_manager.current_state = state
            self.context_state_manager.current_state.enter()
        elif self.parent_state is not None:
            self.parent_state.switch_substate(state)

    def switch_substate(self, state):
        if self.substate is not None:
            self.substate.exit()
        self.substate = state
        self.substate.parent_state = self
        self.substate.enter()
