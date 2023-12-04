import pygame

from Animations.GoblinMoveAnimation import GoblinMoveAnimation
from Enemies.Base.Enemy import Enemy
from Maps.Base.Cell import Cell


class DragonBoss(Enemy):
    default_cooldown_ms = 60000
    default_available_amount = 1
    speed = 0.2
    health = 3000

    def __init__(self, state_context, path_cells):
        self.default_sprite = pygame.image.load("Sprites/Dragon/DragonDefault.png").convert_alpha()
        self.default_sprite = pygame.transform.scale(self.default_sprite, (Cell.screen_size, Cell.screen_size))
        self.move_anim = None
        super().__init__(state_context, self.default_sprite, path_cells, self.move_anim)
