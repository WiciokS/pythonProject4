from Maps.TestMap import TestMap


class LevelBuilder:
    def __init__(self, clock):
        self.level = Level(clock)

    @staticmethod
    def create_level_map(map_name):
        if map_name == "TestMap":
            return TestMap()
        else:
            raise ValueError("Invalid map name")

    def set_difficulty(self, difficulty):
        self.level.difficulty = difficulty

    def add_map(self, map_name):
        self.level.map = LevelBuilder.create_level_map(map_name)

    def add_available_enemy(self, available_enemy):
        self.level.available_enemies.append(available_enemy)

    def add_available_tower(self, available_tower):
        self.level.available_towers.append(available_tower)

    def build(self):
        for i in range(len(self.level.available_enemies)):
            self.level.deployed_enemy_times.append(0)
        return self.level


class Level:
    def __init__(self, clock):
        self.clock = clock
        self.time_ms = 0
        self.map = None
        self.difficulty = 1
        self.deployed_towers = []
        self.deployed_enemies = []
        self.deploy_cooldown = 3000 / self.difficulty

        self.available_towers = []

        # Index would indicate how far in the game the enemy is available
        self.available_enemies = []

        # Index would indicate how many times the index of available_enemies has # been deployed
        self.deployed_enemy_times = []

    def tick(self):
        self.clock.tick()
        self.time_ms += self.clock.get_time()
        self.deploy_cooldown -= self.clock.get_time()
        if self.deploy_cooldown <= 0:
            self.deploy_cooldown = 3000 / self.difficulty
            self.enemy_event()

    def deploy_tower(self, tower, cell):
        self.deployed_towers.append(tower(cell))

    def deploy_enemy(self, enemy):
        self.deployed_enemies.append(enemy)

    def enemy_event(self):
        if len(self.available_enemies) == 0:
            return
        if len(self.available_enemies) > 0:
            if self.deployed_enemy_times[0] < 3:
                self.deployed_enemy_times[0] += 1
                self.deploy_enemy(self.available_enemies[0](self.map.get_path()))
