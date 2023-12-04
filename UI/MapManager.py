import os
import json
import pygame

class MapManager:
    def __init__(self):
        self.maps = {}

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
        map_name = map_data.get('name', os.path.basename(data_path).split('.')[0])

        # Save the map data
        self.maps[map_name] = {
            'image': map_image,
            'data': map_data
        }

    def get_map(self, map_name):
        # Return the map data
        return self.maps.get(map_name)

    def get_maps(self):
        # Return a list of all maps
        return list(self.maps.values())

    def draw_maps_in_row(self, screen, x_position=0, y_position=0, x_offset=0):
        # Iterate over each map image and blit it to the screen at the calculated position
        for map_details in self.get_maps():
            map_image = map_details['image']
            # Blit the map image at the current position
            screen.blit(map_image, (x_position, y_position))
            # Update the x_position for the next map image to be the width of the current one
            x_position += map_image.get_width() + x_offset

    # create method which returns the json file of the map
    def get_map_json(self, map_name):
        return self.maps[map_name]['data']['map']