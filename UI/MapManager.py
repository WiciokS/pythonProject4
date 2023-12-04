import os
import json
import pygame

class MapManager:
    def __init__(self, image_dir, data_dir, screen, scale_size=None, x_offset=40, y_offset=40):
        self.maps = {}
        self.screen = screen
        self.scale_size = scale_size
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.load_all_maps(image_dir, data_dir)

    def load_all_maps(self, image_dir, data_dir):
        # List all .png files in the image directory and corresponding .json files in the data directory
        for file in os.listdir(image_dir):
            if file.endswith('.png'):
                image_path = os.path.join(image_dir, file)
                data_path = os.path.join(data_dir, file.replace('.png', '.json'))
                if os.path.isfile(data_path):
                    self.load_map(image_path, data_path, self.scale_size)

    def load_map(self, image_path, data_path, scale_size=None):
        # Load the map image
        map_image = pygame.image.load(image_path).convert_alpha()

        # Scale the image if a new size is provided
        if scale_size is not None:
            map_image = pygame.transform.scale(map_image, scale_size)

        # Load the map data
        with open(data_path, 'r') as file:
            map_data = json.load(file)

        # If there's no 'name' key, use the file's base name as the map name
        map_name = map_data.get('name', os.path.basename(image_path).split('.')[0])

        # Create a rect for the map image, useful for drawing and collision detection
        map_rect = map_image.get_rect()

        # Save the map data with image and rect
        self.maps[map_name] = {
            'image': map_image,
            'data': map_data,
            'rect': map_rect
        }

    def get_map(self, map_name):
        # Return the map data
        return self.maps.get(map_name)

    def get_maps(self):
        # Return a list of all maps
        return list(self.maps.values())

    def draw_maps_in_row(self, start_x, start_y):
        x_position = start_x
        y_position = start_y
        # Iterate over each map image and blit it to the screen at the calculated position
        for map_details in self.get_maps():
            map_image = map_details['image']
            map_rect = map_details['rect']
            map_rect.topleft = (x_position, y_position)
            self.screen.blit(map_image, map_rect)
            # Update the x_position for the next map image
            x_position += map_rect.width + self.x_offset