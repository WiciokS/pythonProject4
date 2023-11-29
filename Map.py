import pygame
import sys


class Map:
    def __init__(self, path):
        self.path = path

    def draw(self, screen):
        # Clear screen
        screen.fill((128, 128, 128))
        # Check if the path has at least two points to draw a line
        if len(self.path) > 1:
            pygame.draw.lines(screen, (0, 0, 0), False, self.path, 5)

