import pygame

from Enemies.Goblin import Goblin
from Enemies.Orc import Orc
from Level import LevelBuilder
from LevelLoader import LevelLoader
from States.State import StateFactory
from Wave import WaveBuilder


class GameVar:
    def __init__(self, state_context):
        self.state_context = state_context
        self.level = None
        self.selected_tower = None
        self.input_areas = []

        # TODO: Remove temporary level loading
        level_loader = LevelLoader()
        level_loader.convert_level_file("Test.json")

        level_builder = LevelBuilder(state_context)
        level_builder.add_map(level_loader.get_map())
        level_builder.set_starting_gold(level_loader.get_starting_gold())
        for available_tower in level_loader.get_available_towers():
            level_builder.add_available_tower(level_loader.get_tower_class_by_name(available_tower["name"]))
        wave_builder = WaveBuilder(state_context)
        for waves in level_loader.get_waves():
            if waves["number"] != -1:
                for enemy in waves["enemies"]:
                    wave_builder.add_wave_enemy(level_loader.get_enemy_class_by_name(enemy["name"]), enemy["amount"],
                                                enemy["cooldown"], enemy["first_appearance"])
                level_builder.add_wave(wave_builder.build())
                wave_builder.clear()
            else:
                level_builder.add_wave(-1)
                break

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
        self.app_var = AppVar(self)
        self.current_state_root = StateFactory.create_state(state_name, self)
        self.persistent_states = []
        self.game_var = GameVar(self)

        self.current_state_root.enter()

    def tick(self):
        self.app_var.app_clock.tick(self.app_var.fps)
        self.app_var.events = pygame.event.get()
        for event in self.app_var.events:
            if event.type == pygame.QUIT:
                self.app_var.app_running = False
        self.current_state_root.tick()
