import pygame

from Animations.Base.Animation import Animation
from Maps.Base.Cell import Cell


class ArrowBulletFlyingAnimation(Animation):
    delay_tick = 30
    loop = True

    def __init__(self):
        frames = []
        for i in range(1, 3):
            frame = pygame.image.load(
                f"Sprites/Projectile/ArrowBullet/Flying/ArcherBulletFlyingFrame{i}.png").convert_alpha()
            frames.append(pygame.transform.scale(frame, (Cell.screen_size, Cell.screen_size)))

        super().__init__(frames)
