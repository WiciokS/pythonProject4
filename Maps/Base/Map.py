import pygame

from Maps.Base.Cell import Cell


class Map(pygame.sprite.Sprite):
    def __init__(self, path_logical_map_coordinates, cells, map_sprite, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.map_sprite = map_sprite
        self.cells = cells
        self.width = width
        self.height = height
        self.path_cells = self.convert_logical_map_coordinates_to_cells(path_logical_map_coordinates)
        if len(self.path_cells) < 2:
            raise Exception("Path must have at least two points.")
        for i in range(len(self.path_cells) - 1):
            min_x = min(self.path_cells[i].get_logical_map_x(), self.path_cells[i+1].get_logical_map_x())
            max_x = max(self.path_cells[i].get_logical_map_x(), self.path_cells[i+1].get_logical_map_x())
            min_y = min(self.path_cells[i].get_logical_map_y(), self.path_cells[i+1].get_logical_map_y())
            max_y = max(self.path_cells[i].get_logical_map_y(), self.path_cells[i+1].get_logical_map_y())
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    for cell in self.cells:
                        if cell.get_logical_map_x() == x and cell.get_logical_map_y() == y:
                            cell.buildable = False

    def draw(self, screen):
        # Clear screen
        screen.blit(self.map_sprite, (0, 0))

    def get_path(self):
        return self.path_cells

    def get_cell(self, x, y):
        for cell in self.cells:
            if cell.get_logical_map_x() == x and cell.get_logical_map_y() == y:
                return cell
        return None

    def convert_logical_map_coordinates_to_cells(self, path_logical_map_coordinates):
        cells = []
        for point in path_logical_map_coordinates:
            cells.append(self.get_cell(point[0], point[1]))
        return cells

    def convert_screen_coordinates_to_cells(self, screen_coordinates):
        return self.convert_logical_map_coordinates_to_cells(
            self.convert_screen_coordinates_to_logical_map_coordinates(screen_coordinates))

    @staticmethod
    def convert_cells_to_logical_map_coordinates(path_cells):
        coordinates = []
        for cell in path_cells:
            coordinates.append((cell.get_logical_map_x(), cell.get_logical_map_y()))
        return coordinates

    @staticmethod
    def convert_logical_map_coordinates_to_screen_coordinates(logical_map_coordinates):
        map_coordinates = []
        for coordinate in logical_map_coordinates:
            map_coordinates.append(
                (Cell.screen_size / 2 + Cell.screen_size * coordinate[0],
                 Cell.screen_size / 2 + Cell.screen_size * coordinate[1]))
        return map_coordinates

    @staticmethod
    def convert_cells_to_screen_coordinates(path_cells):
        return Map.convert_logical_map_coordinates_to_screen_coordinates(
            Map.convert_cells_to_logical_map_coordinates(path_cells))

    @staticmethod
    def convert_screen_coordinates_to_logical_map_coordinates(screen_coordinates):
        logical_coordinates = [(int(screen_coordinates[0] / Cell.screen_size),
                                int(screen_coordinates[1] / Cell.screen_size))]
        return logical_coordinates
