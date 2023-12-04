import pygame

from Animations.Base.Animation import Animation
from Maps.Base.Cell import Cell


class WaterElementalAttackAnimation(Animation):
    delay_tick = 30
    loop = False

    def __init__(self):
        frame = pygame.image.load(f"Sprites/WaterElemental/Attack/Frame1.png").convert_alpha()
        frames = [pygame.transform.scale(frame, (Cell.screen_size, Cell.screen_size))]

        super().__init__(frames)
