from GameplayState import GameplayState, UnpausedGameplayState, PausedGameplayState
from State import StateName


class StateFactory:
    @staticmethod
    def create_state(state_name, context):
        if state_name == StateName.GAMEPLAY:
            return GameplayState(context)
        elif state_name == StateName.UNPAUSED_GAMEPLAY:
            return UnpausedGameplayState(context)
        elif state_name == StateName.PAUSED_GAMEPLAY:
            return PausedGameplayState(context)
        else:
            raise ValueError("Invalid state name")


class StateManager:
    def __init__(self, default_state):
        self.current_state = default_state
        self.persistent_state = None
        self.current_state.enter()
        pass

    def switch_states(self, state):
        self.current_state.exit()
        self.current_state = state
        self.current_state.enter()

    def tick(self):
        self.current_state.tick()
