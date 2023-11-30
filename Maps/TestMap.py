from Cell import Cell
from Map import Map


class TestMap(Map):
    def __init__(self):
        # Create cells
        cells = []
        for y in range(10):
            for x in range(10):
                cells.append(Cell(x, y, True))

        # Create path for enemies
        enemy_path_logical_map_coordinates = [(0, 0), (9, 0), (9, 9), (0, 9)]
        super().__init__(enemy_path_logical_map_coordinates, cells)
