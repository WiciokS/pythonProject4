import pygame


class Cell:
    screen_size = 50

    def __init__(self, logical_map_x, logical_map_y, buildable=True, screen_size=50):
        self.logical_map_x = logical_map_x
        self.logical_map_y = logical_map_y
        Cell.screen_size = screen_size
        self.buildable = buildable

    def get_screen_x(self):
        return self.screen_size / 2 + self.screen_size * self.logical_map_x

    def get_screen_y(self):
        return self.screen_size / 2 + self.screen_size * self.logical_map_y

    def get_logical_map_x(self):
        return self.logical_map_x

    def get_logical_map_y(self):
        return self.logical_map_y

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0),
                         (self.get_screen_x() - self.screen_size / 2, self.get_screen_y() - self.screen_size / 2,
                          self.screen_size, self.screen_size), 1)
