import pygame


class Cell:
    size = 50

    def __init__(self, logicalX, logicalY, buildable=True, size=50):
        self.logicalX = logicalX
        self.logicalY = logicalY
        Cell.size = size
        self.buildable = buildable

    def get_map_x(self):
        return self.size / 2 + self.size * self.logicalX

    def get_map_y(self):
        return self.size / 2 + self.size * self.logicalY

    def get_logical_x(self):
        return self.logicalX

    def get_logical_y(self):
        return self.logicalY

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.get_map_x() - self.size / 2, self.get_map_y() - self.size / 2,
                                             self.size, self.size), 1)
