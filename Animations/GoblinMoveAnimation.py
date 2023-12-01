import pygame

from Animations.Base.Animation import Animation


class GoblinMoveAnimation(Animation):
    delay_tick = 30
    loop = True

    def __init__(self):
        frames = []
        for i in range(1, 5):
            frames.append(pygame.image.load(f"Sprites/Goblin/MoveAnim/Frame{i}.png").convert_alpha())

        super().__init__(frames)
