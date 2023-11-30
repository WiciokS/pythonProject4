import pygame

from Cell import Cell


class Map:
    def __init__(self, path_logical_map_coordinates, cells):
        self.cells = cells
        self.path_cells = self.convert_logical_map_coordinates_to_cells(path_logical_map_coordinates)

    def draw(self, screen):
        # Clear screen
        screen.fill((128, 128, 128))

        # Draw cell outlines
        for cell in self.cells:
            cell.draw(screen)

        # Check if the path has at least two points to draw a line
        if len(self.path_cells) > 1:
            pygame.draw.lines(screen, (0, 0, 0), False, self.convert_cells_to_screen_coordinates(self.path_cells), 5)

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
        logical_coordinates = []
        for coordinate in screen_coordinates:
            logical_coordinates.append((int(coordinate[0] / Cell.screen_size), int(coordinate[1] / Cell.screen_size)))
        return logical_coordinates
