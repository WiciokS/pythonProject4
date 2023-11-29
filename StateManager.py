
class StateManager:
    def __init__(self, default_state):
        self.current_state = default_state
        self.current_state.enter()
        pass

    def switch_states(self, state):
        self.current_state.exit()
        self.current_state = state
        self.current_state.enter()

    def tick(self):
        self.current_state.tick()
