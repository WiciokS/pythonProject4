import pygame

from Animations.Base.Animation import Animation
from Maps.Base.Cell import Cell


class OrcMoveAnimation(Animation):
    delay_tick = 30
    loop = True

    def __init__(self):
        frames = []
        for i in range(1, 5):
            frame = pygame.image.load(f"Sprites/Orc/MoveAnim/Frame{i}.png").convert_alpha()
            frames.append(pygame.transform.scale(frame, (Cell.screen_size, Cell.screen_size)))

        super().__init__(frames)
