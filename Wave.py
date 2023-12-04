import random

from Enemies.Dragon import Dragon
from Enemies.Goblin import Goblin
from Enemies.Orc import Orc


class Wave:
    def __init__(self, state_context):
        self.state_context = state_context
        self.time_ms = 0

        # Enemies
        self.deployed_wave_enemies = []  # Deployed enemies

        self.available_wave_enemies = []  # Available enemies

        self.available_wave_enemies_cooldown_constant = []  # Constant cooldown for each enemy

        self.available_wave_enemies_cooldown_interactive = []  # Dynamic cooldown for each enemy

        self.available_wave_enemies_available_amount = []  # Available amount of each enemy

        self.available_wave_enemies_deployed_times = []  # How many times have each enemy been deployed

    def tick(self):
        self.time_ms += self.state_context.app_var.app_clock.get_time()
        for i in range(len(self.available_wave_enemies)):
            if self.available_wave_enemies_available_amount[i] > 0:
                self.available_wave_enemies_cooldown_interactive[i] -= self.state_context.app_var.app_clock.get_time()
                if self.available_wave_enemies_cooldown_interactive[i] <= 0:
                    self.deploy_enemy(self.available_wave_enemies[i])
                    self.available_wave_enemies_cooldown_interactive[i] = self.available_wave_enemies_cooldown_constant[
                        i]
                    self.available_wave_enemies_available_amount[i] -= 1

    def deploy_enemy(self, enemy):
        self.deployed_wave_enemies.append(enemy(self.state_context, self.state_context.game_var.level.map.path_cells))

    def wave_completed(self):
        for i in range(len(self.available_wave_enemies)):
            if self.available_wave_enemies_available_amount[i] > 0:
                return False
        if len(self.deployed_wave_enemies) > 0:
            return False
        self.time_ms = 0
        return True


class WaveBuilder:
    def __init__(self, state_context):
        self.wave = Wave(state_context)

    def add_wave_enemy(self, wave_enemy, available_amount=-1, cooldown_ms=-1, first_appearance_ms=-1):
        if available_amount == -1:
            self.wave.available_wave_enemies_available_amount.append(wave_enemy.default_available_amount)
        else:
            self.wave.available_wave_enemies_available_amount.append(available_amount)

        if cooldown_ms == -1:
            self.wave.available_wave_enemies_cooldown_constant.append(wave_enemy.default_cooldown_ms)
            self.wave.available_wave_enemies_cooldown_interactive.append(wave_enemy.default_cooldown_ms)
        else:
            self.wave.available_wave_enemies_cooldown_constant.append(cooldown_ms)
            if first_appearance_ms == -1:
                self.wave.available_wave_enemies_cooldown_interactive.append(cooldown_ms)
            else:
                self.wave.available_wave_enemies_cooldown_interactive.append(first_appearance_ms)

        self.wave.available_wave_enemies.append(wave_enemy)

    def create_random_wave(self, possible_enemies=None):
        rng = random.randint(100, 1000)
        temp_possible_enemies = []
        if possible_enemies is None:
            temp_possible_enemies.append(Goblin)
            temp_possible_enemies.append(Orc)
            temp_possible_enemies.append(Dragon)
        else:
            temp_possible_enemies = possible_enemies

        for enemy in temp_possible_enemies:
            rng_adjust = rng // enemy.health
            if rng_adjust <= 0:
                rng_adjust = 1
            rng_cd = 1000
            if enemy.__class__.__name__ == "Goblin":
                rng_cd = random.randint(Goblin.default_cooldown_ms//2, Goblin.default_cooldown_ms*2)
            elif enemy.__class__.__name__ == "Orc":
                rng_cd = random.randint(Orc.default_cooldown_ms//2, Orc.default_cooldown_ms*2)
            elif enemy.__class__.__name__ == "Dragon":
                rng_cd = random.randint(Dragon.default_cooldown_ms//2, Dragon.default_cooldown_ms*2)
            self.add_wave_enemy(enemy, available_amount=rng_adjust, cooldown_ms=rng_cd)

    def build(self):
        for i in range(len(self.wave.available_wave_enemies)):
            self.wave.available_wave_enemies_deployed_times.append(0)
        return self.wave

    def clear(self):
        state_context = self.wave.state_context
        self.wave = Wave(state_context)
