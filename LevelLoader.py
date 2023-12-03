import json


class LevelLoader:
    def __init__(self):
        self.level_file = None

    def convert_level_file(self, file_name):
        file = open("Levels/" + file_name, 'r')
        data = json.load(file)
        file.close()
        self.level_file = data

    def get_level_file(self):
        return self.level_file

    def get_map(self):
        return self.level_file["map"]

    def get_starting_gold(self):
        return self.level_file["starting_gold"]

    def get_waves(self):
        return self.level_file["waves"]

    def get_available_towers(self):
        return self.level_file["available_towers"]

    def get_wave_number(self, index):
        return self.level_file["waves"][index]["number"]

    def get_wave_enemies(self, index):
        return self.level_file["waves"][index]["enemies"]

    def get_wave_enemy(self, index, enemy_index):
        return self.level_file["waves"][index]["enemies"][enemy_index]

    def get_wave_enemy_name(self, index, enemy_index):
        return self.level_file["waves"][index]["enemies"][enemy_index]["name"]

    def get_wave_enemy_amount(self, index, enemy_index):
        return self.level_file["waves"][index]["enemies"][enemy_index]["amount"]

    def get_wave_enemy_cooldown(self, index, enemy_index):
        return self.level_file["waves"][index]["enemies"][enemy_index]["cooldown"]

    def get_wave_enemy_first_appearance(self, index, enemy_index):
        return self.level_file["waves"][index]["enemies"][enemy_index]["first_appearance"]

    @staticmethod
    def get_enemy_class_by_name(name):
        if name == "Goblin":
            from Enemies.Goblin import Goblin
            return Goblin
        elif name == "Orc":
            from Enemies.Orc import Orc
            return Orc
        else:
            raise ValueError("Invalid enemy name")

    @staticmethod
    def get_tower_class_by_name(name):
        if name == "Archer":
            from Towers.Archer import Archer
            return Archer
        elif name == "Mage":
            from Towers.Mage import Mage
            return Mage
        elif name == "WaterElemental":
            from Towers.WaterElemental import WaterElemental
            return WaterElemental
        else:
            raise ValueError("Invalid tower name")