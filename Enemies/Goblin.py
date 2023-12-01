import pygame

from Animations.GoblinMoveAnimation import GoblinMoveAnimation
from Enemies.Base.Enemy import Enemy
from Maps.Base.Cell import Cell


class Goblin(Enemy):
    default_cooldown_ms = 3000
    default_available_amount = 99999
    speed = 1
    health = 10

    def __init__(self, path_cells):
        self.default_sprite = pygame.image.load("Sprites/Goblin/GoblinDefault.png").convert_alpha()
        self.default_sprite = pygame.transform.scale(self.default_sprite, (Cell.screen_size, Cell.screen_size))
        self.move_anim = GoblinMoveAnimation()
        super().__init__(self.default_sprite, path_cells, self.move_anim)
