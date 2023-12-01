import pygame

from Enemies.Goblin import Goblin
from Enemies.Orc import Orc
from Level import LevelBuilder
from States.State import StateFactory
from Towers.Mage import Mage
from Towers.ArcherTower import ArcherTower
from Towers.ElementalTower import ElementalTower


class GameVar:
    def __init__(self, state_context):
        self.state_context = state_context
        self.level = None
        self.selected_tower = None
        self.input_areas = []

        # TODO: Remove this
        level_builder = LevelBuilder(pygame.time.Clock())
        level_builder.add_map("TestMap")
        level_builder.add_available_enemy(Goblin)
        level_builder.add_available_enemy(Orc)
        level_builder.add_available_tower(Mage)
        #level_builder.add_available_tower(ArcherTower)
        #level_builder.add_available_tower(ElementalTower)
        self.level = level_builder.build()


class AppVar:
    def __init__(self, state_context):
        self.state_context = state_context
        self.app_clock = pygame.time.Clock()
        self.app_running = False
        self.fps = 60
        self.screen = pygame.display.set_mode((1280, 640))
        self.events = None


class StateContext:
    def __init__(self, state_name):
        self.current_state_root = StateFactory.create_state(state_name, self)
        self.persistent_states = []
        self.app_var = AppVar(self)
        self.game_var = GameVar(self)

        self.current_state_root.enter()

    def tick(self):
        self.app_var.app_clock.tick(self.app_var.fps)
        self.app_var.events = pygame.event.get()
        for event in self.app_var.events:
            if event.type == pygame.QUIT:
                self.app_var.app_running = False
        self.current_state_root.tick()
