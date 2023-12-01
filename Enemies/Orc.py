import pygame

from Animations.OrcMoveAnimation import OrcMoveAnimation
from Enemies.Base.Enemy import Enemy
from Maps.Base.Cell import Cell


class Orc(Enemy):
    default_cooldown_ms = 7000
    default_available_amount = 99999
    speed = 0.5

    def __init__(self, path_cells):
        self.default_sprite = pygame.image.load("Sprites/Orc/OrcDefault.png").convert_alpha()
        self.default_sprite = pygame.transform.scale(self.default_sprite, (Cell.screen_size, Cell.screen_size))
        self.move_anim = OrcMoveAnimation()
        super().__init__(self.default_sprite, self.move_anim, path_cells)
