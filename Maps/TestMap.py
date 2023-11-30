import pygame

from Maps.Base.Cell import Cell
from Maps.Base.Map import Map


class TestMap(Map):
    def __init__(self):
        self.map_sprite = pygame.image.load("Maps/TestMap.png")

        # Create cells
        cells = []
        for y in range(20):
            for x in range(30):
                cells.append(Cell(x, y, True))

        # Create path for enemies
        enemy_path_logical_map_coordinates = [(26, 0), (26, 9), (15, 9), (15, 2), (2, 2), (2, 16), (25, 16), (25, 19)]
        super().__init__(enemy_path_logical_map_coordinates, cells, self.map_sprite)
