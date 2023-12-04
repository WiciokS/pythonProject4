import pygame

from Maps.Base.Cell import Cell


class Enemy(pygame.sprite.Sprite):
    default_cooldown_ms = 3000
    default_available_amount = 99999
    speed = 1
    health = 100

    def __init__(self, state_context, default_sprite, path_cells, move_anim=None):
        pygame.sprite.Sprite.__init__(self)
        self.state_context = state_context
        self.default_health = self.health
        self.default_speed = self.speed
        self.default_sprite = default_sprite
        self.rect = self.default_sprite.get_rect()

        self.move_anim = move_anim

        self.path_cells = path_cells
        self.path_index = 0

        self.screen_position = pygame.Vector2((path_cells[0].get_screen_x(), path_cells[0].get_screen_y()))

        self.push_speed = 8
        self.push_distance_screen_x = 0
        self.push_distance_screen_y = 0
        self.push_tick = False

    def tick(self):
        if self.health <= 0:
            self.death()
            return
        self.move()

    def move(self):
        if self.move_anim is not None and not self.move_anim.playing:
            self.move_anim.play()

        # Move the enemy smoothly along the path
        target_screen_position = pygame.Vector2(
            (self.path_cells[self.path_index].get_screen_x(), self.path_cells[self.path_index].get_screen_y()))

        movement = target_screen_position - self.screen_position

        if self.push_tick:  # If we're being pushed, move in the direction of the push
            direction = movement.normalize()
            if self.push_distance_screen_x > 0:
                self.speed += direction[0] * self.push_speed
                self.push_distance_screen_x -= self.push_speed
            elif self.push_distance_screen_x < 0:
                self.speed -= direction[0] * self.push_speed
                self.push_distance_screen_x += self.push_speed
            if self.push_distance_screen_y > 0:
                self.speed += direction[1] * self.push_speed
                self.push_distance_screen_y -= self.push_speed
            elif self.push_distance_screen_y < 0:
                self.speed -= direction[1] * self.push_speed
                self.push_distance_screen_y += self.push_speed

        if movement.length() > self.speed:  # If we're not at the target, move towards it
            movement = movement.normalize() * self.speed
            self.screen_position += movement
        else:  # If we've reached the target, move to the next point
            self.screen_position = target_screen_position
            self.path_index += 1

        if self.push_tick:
            if (abs(self.push_distance_screen_x) < self.push_speed and
                    abs(self.push_distance_screen_y) < self.push_speed):
                self.push_tick = False
                self.speed = self.default_speed

        if self.move_anim is not None:
            self.move_anim.tick()

        self.rect.center = (int(self.screen_position.x), int(self.screen_position.y))

    def place_on_start_point(self):
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

    def death(self):
        self.state_context.game_var.level.gold += self.default_health // 3
        self.remove()

    def remove(self):
        # Remove the enemy from the wave
        if self.state_context.game_var.level.current_wave_index < len(self.state_context.game_var.level.waves):
            self.state_context.game_var.level.waves[
                self.state_context.game_var.level.current_wave_index].deployed_wave_enemies.remove(self)
        # Remove the enemy from towers' possible targets and target
        for tower in self.state_context.game_var.level.deployed_towers:
            if self in tower.possible_targets:
                tower.possible_targets.remove(self)
            if tower.target is self:
                tower.target = None
        del self

    def at_end_of_path(self):
        return self.path_index > len(self.path_cells) - 1

    def push(self, x=0, y=0):
        self.push_distance_screen_x = x
        self.push_distance_screen_y = y
        self.push_tick = True
