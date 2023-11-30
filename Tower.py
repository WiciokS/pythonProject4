import pygame
import sys


class Tower:
    def __init__(self, cell):
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 128, 0))
        self.rect = self.image.get_rect(center=(cell.get_screen_x(), cell.get_screen_y()))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

