import pygame


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.screen_position = pygame.Vector2((self.x, self.y))

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
