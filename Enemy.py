import pygame
import sys


class Enemy:
    def __init__(self, path):
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=path[0])
        self.path = path
        self.path_index = 0
        self.position = pygame.Vector2(path[0])  # Use vectors for smooth movement
        self.speed = 1

    def move(self):
        # Move the enemy smoothly along the path
        target_position = pygame.Vector2(self.path[self.path_index])
        movement = target_position - self.position
        if movement.length() > self.speed:  # If we're not at the target, move towards it
            movement = movement.normalize() * self.speed
            self.position += movement
        else:  # If we've reached the target, move to the next point
            self.position = target_position
            self.path_index += 1

        self.rect.center = (int(self.position.x), int(self.position.y))  # Update the rect for drawing

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def at_end_of_path(self):
        return
