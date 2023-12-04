import pygame

from Maps.BlueMagicMap import BlueMagicMap
from Maps.TestMap import TestMap
from Wave import WaveBuilder


class LevelBuilder:
    def __init__(self, state_context):
        self.level = Level(state_context)

    @staticmethod
    def create_level_map(map_name):
        if map_name == "TestMap":
            return TestMap()
        elif map_name == "BlueMagicMap":
            return BlueMagicMap()
        else:
            raise ValueError("Invalid map name")

    def add_map(self, map_name):
        self.level.map = LevelBuilder.create_level_map(map_name)

    def add_available_tower(self, available_tower):
        self.level.available_towers.append(available_tower)

    def add_wave(self, wave):
        if wave == -1:
            waveBuilder = WaveBuilder(self.level.state_context)
            waveBuilder.create_random_wave()
            self.level.infinite_waves = True
            self.level.waves.append(waveBuilder.build())
            return
        self.level.waves.append(wave)

    def set_starting_gold(self, starting_gold):
        self.level.gold = starting_gold

    def build(self):
        return self.level


class Level:
    def __init__(self, state_context):
        self.state_context = state_context

        self.map = None
        self.gold = 0

        # Towers
        self.deployed_towers = []  # Deployed towers

        self.available_towers = []  # Available towers

        self.projectiles = []  # Projectiles

        # Waves
        self.waves = []
        self.current_wave_index = 0

        self.infinite_waves = False

    def tick(self):
        if self.current_wave_index < len(self.waves):
            if not self.waves[self.current_wave_index].wave_completed():
                self.waves[self.current_wave_index].tick()

    def next_wave(self):
        if self.current_wave_index < len(self.waves):
            if self.infinite_waves:
                waveBuilder = WaveBuilder(self.state_context)
                waveBuilder.create_random_wave()
                self.waves.append(waveBuilder.build())
            self.current_wave_index += 1

    def completed(self):
        return self.current_wave_index >= len(self.waves)

    def deploy_tower(self, tower, cell):
        self.deployed_towers.append(tower(cell))
