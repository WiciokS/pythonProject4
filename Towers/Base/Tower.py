import pygame

from Maps.Base.Cell import Cell


class Tower(pygame.sprite.Sprite):
    def __init__(self, cell, default_sprite):
        pygame.sprite.Sprite.__init__(self)
        self.cell = cell
        self.default_sprite = default_sprite
        self.rect = self.default_sprite.get_rect()
        if cell is not None:
            self.rect.center = (cell.get_screen_x(), cell.get_screen_y())

    def draw(self, screen):
        screen.blit(self.default_sprite, self.rect)

    def place(self, cell):
        self.cell = cell
        self.rect.center = (cell.get_screen_x(), cell.get_screen_y())
        self.cell.tower = self

    def remove(self):
        if self.cell is not None:
            self.cell.tower = None
            self.cell = None


