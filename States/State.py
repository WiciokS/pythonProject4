from abc import ABC, abstractmethod
from enum import Enum


class StateFactory:
    @staticmethod
    def create_state(state_name, context_state_manager):
        if state_name == StateName.GAMEPLAY:
            from States.GameplayStates import GameplayState
            return GameplayState(context_state_manager)
        elif state_name == StateName.PAUSE:
            from States.MenuStates import PausedState
            return PausedState(context_state_manager)
        elif state_name == StateName.ACTIVE_GAME:
            from States.GameplayStates import ActiveGameState
            return ActiveGameState(context_state_manager)
        elif state_name == StateName.PREPARE_GAME:
            from States.GameplayStates import PrepareGameState
            return PrepareGameState(context_state_manager)
        else:
            raise ValueError("Invalid state name")


class StateName(Enum):
    MAIN_MENU = 0
    GAMEPLAY = 1
    ACTIVE_GAME = 10
    PREPARE_GAME = 11
    PAUSE = 2


class State(ABC):
    def __init__(self, state_name, context_state_manager, root_state=True):
        self.root_state = root_state
        self.state_name = state_name
        self.state_context = context_state_manager
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
        if self not in self.state_context.persistent_states:
            self.exit()
        if self.root_state:
            if state not in self.state_context.persistent_states:
                state.enter()
            self.state_context.current_state_root = state
        elif self.parent_state is not None:
            self.parent_state.switch_substate(state)

    def switch_substate(self, state):
        if self.substate is not None:
            if self not in self.state_context.persistent_states:
                self.substate.exit()
        if state not in self.state_context.persistent_states:
            state.enter()
        self.substate = state
        self.substate.parent_state = self
