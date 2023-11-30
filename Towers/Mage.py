import pygame

from Maps.Base.Cell import Cell
from Towers.Base.Tower import Tower


class Mage(Tower):
    def __init__(self, cell=None):
        self.default_sprite = pygame.image.load("Sprites/Mage/MageDefault.png").convert_alpha()
        self.default_sprite = pygame.transform.scale(self.default_sprite, (Cell.screen_size, Cell.screen_size))
        super().__init__(cell, self.default_sprite)
