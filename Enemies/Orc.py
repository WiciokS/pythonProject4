import pygame

from Enemies.Base.Enemy import Enemy
from Maps.Base.Cell import Cell


class Orc(Enemy):
    def __init__(self, path_cells):
        self.default_sprite = pygame.image.load("Sprites/Orc/OrcDefault.png").convert_alpha()
        self.default_sprite = pygame.transform.scale(self.default_sprite, (Cell.screen_size, Cell.screen_size))
        super().__init__(path_cells, self.default_sprite)

