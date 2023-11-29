from abc import ABC
from Enemy import Enemy
from Map import Map
from Tower import Tower
from State import State


class GameplayState(State):
    def __init__(self):
        self.tower = Tower((400, 300))
        self.enemy_path = [(100, 100), (700, 100), (700, 500), (100, 500)]
        self.game_map = Map(self.enemy_path)
        self.enemy = Enemy(self.enemy_path)

    def tick(self, screen):
        # Move the enemy if it's not at the end of the path
        if not self.enemy.at_end_of_path():
            self.enemy.move()

        # Draw map
        self.game_map.draw(screen)

        # Draw the tower and the enemy
        self.tower.draw(screen)
        self.enemy.draw(screen)

    def enter(self):
        pass

    def exit(self):
        pass
