from GameplayState import GameplayState, UnpausedGameplayState, PausedGameplayState
from State import StateName


class StateFactory:
    @staticmethod
    def create_state(state_name, context_state_manager):
        if state_name == StateName.GAMEPLAY:
            return GameplayState(context_state_manager)
        elif state_name == StateName.UNPAUSED_GAMEPLAY:
            return UnpausedGameplayState(context_state_manager)
        elif state_name == StateName.PAUSED_GAMEPLAY:
            return PausedGameplayState(context_state_manager)
        else:
            raise ValueError("Invalid state name")


class StateManager:
    def __init__(self, state_name):
        self.time_ms = 0
        self.current_state = StateFactory.create_state(state_name, self)
        self.persistent_state = None
        self.current_state.enter()

    def tick(self):
        self.current_state.tick()
