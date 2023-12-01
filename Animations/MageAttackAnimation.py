import pygame

from Animations.Base.Animation import Animation


class MageAttackAnimation(Animation):
    delay_tick = 30
    loop = False

    def __init__(self):
        frames = [pygame.image.load(f"Sprites/Mage/Attack/Frame1.png").convert_alpha()]

        super().__init__(frames)
