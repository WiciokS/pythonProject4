import pygame

from Maps.TestMap import TestMap


class LevelBuilder:
    def __init__(self, state_context):
        self.level = Level(state_context)

    @staticmethod
    def create_level_map(map_name):
        if map_name == "TestMap":
            return TestMap()
        else:
            raise ValueError("Invalid map name")

    def add_map(self, map_name):
        self.level.map = LevelBuilder.create_level_map(map_name)

    def add_available_enemy(self, available_enemy, available_amount=-1, cooldown_ms=-1):
        if available_amount == -1:
            self.level.available_enemies_available_amount.append(available_enemy.default_available_amount)
        else:
            self.level.available_enemies_available_amount.append(available_amount)
        if cooldown_ms == -1:
            self.level.available_enemies_cooldown_constant.append(available_enemy.default_cooldown_ms)
            self.level.available_enemies_cooldown_interactive.append(available_enemy.default_cooldown_ms)
        else:
            self.level.available_enemies_cooldown_constant.append(cooldown_ms)
            self.level.available_enemies_cooldown_interactive.append(cooldown_ms)

        self.level.available_enemies.append(available_enemy)

    def add_available_tower(self, available_tower):
        self.level.available_towers.append(available_tower)

    def build(self):
        for i in range(len(self.level.available_enemies)):
            self.level.available_enemies_deployed_times.append(0)
        return self.level


class Level:
    def __init__(self, state_context):
        self.state_context = state_context
        self.time_ms = 0
        self.map = None

        # Towers
        self.deployed_towers = []  # Deployed towers

        self.available_towers = []  # Available towers

        self.projectiles = []  # Projectiles

        # Enemies
        self.deployed_enemies = []  # How many times have each enemy been deployed

        self.available_enemies = []  # Available enemies

        self.available_enemies_cooldown_constant = []  # Constant cooldown for each enemy

        self.available_enemies_cooldown_interactive = []  # Dynamic cooldown for each enemy

        self.available_enemies_available_amount = []  # Available amount of each enemy

        self.available_enemies_deployed_times = []  # How many times have each enemy been deployed

    def tick(self):
        self.time_ms += self.state_context.app_var.app_clock.get_time()
        for i in range(len(self.available_enemies)):
            self.available_enemies_cooldown_interactive[i] -= self.state_context.app_var.app_clock.get_time()
            if self.available_enemies_cooldown_interactive[i] <= 0:
                self.deploy_enemy(self.available_enemies[i])
                self.available_enemies_cooldown_interactive[i] = self.available_enemies_cooldown_constant[i]

    def deploy_tower(self, tower, cell):
        self.deployed_towers.append(tower(cell))

    def deploy_enemy(self, enemy):
        self.deployed_enemies.append(enemy(self.state_context, self.map.path_cells))
