import pygame

from Maps.Base.Cell import Cell


class Enemy(pygame.sprite.Sprite):
    default_cooldown_ms = 3000
    default_available_amount = 99999
    speed = 1

    def __init__(self, default_sprite, move_anim, path_cells):
        pygame.sprite.Sprite.__init__(self)
        self.default_sprite = default_sprite
        self.move_anim = move_anim
        self.path_cells = path_cells
        self.rect = self.default_sprite.get_rect()
        self.path_index = 0
        self.screen_position = pygame.Vector2((path_cells[0].get_screen_x(), path_cells[0].get_screen_y()))

    def move(self):
        if self.move_anim is not None and not self.move_anim.playing:
            self.move_anim.play()

        # Orc the enemy smoothly along the path
        target_screen_position = pygame.Vector2(
            (self.path_cells[self.path_index].get_screen_x(), self.path_cells[self.path_index].get_screen_y()))

        movement = target_screen_position - self.screen_position
        if movement.length() > self.speed:  # If we're not at the target, move towards it
            movement = movement.normalize() * self.speed
            self.screen_position += movement
        else:  # If we've reached the target, move to the next point
            self.screen_position = target_screen_position
            self.path_index += 1

        if self.move_anim is not None:
            self.move_anim.tick()

        self.rect.center = (int(self.screen_position.x), int(self.screen_position.y))

    def spawn(self):
        if self.default_sprite is not None:
            self.rect = self.default_sprite.get_rect(
                center=(self.path_cells[0].get_screen_x(), self.path_cells[0].get_screen_y()))

    def draw(self, screen):
        if self.default_sprite is None:
            return
        if self.move_anim is not None and self.move_anim.playing:
            screen.blit(self.move_anim.get_current_frame(), self.rect)
        else:
            screen.blit(self.default_sprite, self.rect)

    def at_end_of_path(self):
        return self.path_index > len(self.path_cells) - 1
