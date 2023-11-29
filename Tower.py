import pygame
import sys


class Tower:
    def __init__(self, position):
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 128, 0))
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
