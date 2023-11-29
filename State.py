from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def tick(self):
        pass

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def exit(self):
        pass
