import pygame

from Maps.Base.Cell import Cell
from Maps.Base.Map import Map


class BlueMagicMap(Map):
    def __init__(self):
        self.map_sprite = pygame.image.load("Maps/Images/BlueMagicMap.png")
        self.map_sprite = pygame.transform.scale(self.map_sprite, (960, 640))

        # Create cells
        cells = []
        for y in range(40):
            for x in range(60):
                buildable = True
                cells.append(Cell(x, y, buildable, 16))

        width = 60 * Cell.screen_size
        height = 40 * Cell.screen_size

        # Create path for enemies
        enemy_path_logical_map_coordinates = [(0, 35), (51, 35), (51, 4), (4, 4), (4, 31), (21, 31), (21, 8), (43, 8),
                                              (43, 24), (59, 24)]
        super().__init__(enemy_path_logical_map_coordinates, cells, self.map_sprite, width, height)
