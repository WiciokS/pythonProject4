import pygame

from Animations.Base.Animation import Animation


class MageBulletFlyingAnimation(Animation):
    delay_tick = 30
    loop = True

    def __init__(self):
        frames = []
        for i in range(1, 3):
            frames.append(pygame.image.load(
                f"Sprites/Projectile/MageBullet/Flying/MageBulletFlyingFrame{i}.png").convert_alpha())

        super().__init__(frames)
