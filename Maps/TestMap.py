import pygame

from Maps.Base.Cell import Cell
from Maps.Base.Map import Map


class TestMap(Map):
    def __init__(self):
        self.map_sprite = pygame.image.load("Maps/Images/TestMap.png")

        # Create cells
        cells = []
        for y in range(20):
            for x in range(30):
                buildable = True
                if 6 <= x <= 11 and 6 <= y <= 11:
                    buildable = False
                cells.append(Cell(x, y, buildable))

        width = 30 * Cell.screen_size
        height = 20 * Cell.screen_size

        # Create path for enemies
        enemy_path_logical_map_coordinates = [(26, 0), (26, 9), (15, 9), (15, 2), (2, 2), (2, 16), (25, 16), (25, 19)]
        super().__init__(enemy_path_logical_map_coordinates, cells, self.map_sprite, width, height)
