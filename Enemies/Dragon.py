import pygame

from Animations.GoblinMoveAnimation import GoblinMoveAnimation
from Enemies.Base.Enemy import Enemy
from Maps.Base.Cell import Cell


class Dragon(Enemy):
    default_cooldown_ms = 60000
    default_available_amount = 1
    speed = 0.2
    health = 3000

    def __init__(self, state_context, path_cells):
        self.default_sprite = pygame.image.load("Sprites/Dragon/DragonDefault.png").convert_alpha()
        self.default_sprite = pygame.transform.scale(self.default_sprite, (Cell.screen_size * 3, Cell.screen_size * 3))
        self.move_anim = None
        super().__init__(state_context, self.default_sprite, path_cells, self.move_anim)
