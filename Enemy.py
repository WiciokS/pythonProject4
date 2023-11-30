import pygame


class Enemy:
    def __init__(self, path_cells):
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(path_cells[0].get_screen_x(), path_cells[0].get_screen_y()))
        self.path_cells = path_cells
        self.path_index = 0
        self.screen_position = pygame.Vector2((path_cells[0].get_screen_x(), path_cells[0].get_screen_y()))  # Use vectors for smooth movement
        self.speed = 1

    def move(self):
        # Move the enemy smoothly along the path
        target_screen_position = pygame.Vector2((self.path_cells[self.path_index].get_screen_x(), self.path_cells[self.path_index].get_screen_y()))
        movement = target_screen_position - self.screen_position
        if movement.length() > self.speed:  # If we're not at the target, move towards it
            movement = movement.normalize() * self.speed
            self.screen_position += movement
        else:  # If we've reached the target, move to the next point
            self.screen_position = target_screen_position
            self.path_index += 1

        self.rect.center = (int(self.screen_position.x), int(self.screen_position.y))  # Update the rect for drawing

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def at_end_of_path(self):
        return self.path_index > len(self.path_cells) - 1


