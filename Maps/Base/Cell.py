import pygame


class Cell:
    screen_size = 32
    buildable_color = (0, 255, 0)
    not_buildable_color = (255, 0, 0)

    def __init__(self, logical_map_x, logical_map_y, buildable=True, screen_size=32):
        self.logical_map_x = logical_map_x
        self.logical_map_y = logical_map_y
        self.tower = None
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

    def remove_tower(self):
        if self.tower is not None:
            self.tower.remove()
            self.tower = None

    def draw(self, screen):
        color = Cell.buildable_color if self.buildable else Cell.not_buildable_color
        pygame.draw.rect(screen, color,
                         (self.get_screen_x() - self.screen_size / 2, self.get_screen_y() - self.screen_size / 2,
                          self.screen_size, self.screen_size), 1)
