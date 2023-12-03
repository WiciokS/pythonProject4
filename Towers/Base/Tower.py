from abc import abstractmethod

import pygame

from Maps.Base.Cell import Cell


class Tower(pygame.sprite.Sprite):
    action_cooldown_ms = 1000
    range = 1
    cost = 100
    icon_path = None

    def __init__(self, state_context, cell, default_sprite, action_anim=None, ):
        self.state_context = state_context
        pygame.sprite.Sprite.__init__(self)
        self.cell = cell
        self.last_cell = None
        self.action_cooldown_ms_interactive = self.action_cooldown_ms
        self.default_sprite = default_sprite
        self.action_anim = action_anim
        self.rect = self.default_sprite.get_rect()
        self.possible_targets = []
        self.target = None
        if self.cell is not None:
            self.rect.center = (cell.get_screen_x(), cell.get_screen_y())
            self.cell.tower = self
        self.range_circle = pygame.Surface((10 * self.range * Cell.screen_size,
                                            10 * self.range * Cell.screen_size),
                                           pygame.SRCALPHA)
        self.screen_position = pygame.Vector2((self.rect.centerx, self.rect.centery))

    def draw(self, screen):
        if self.action_anim is not None and self.action_anim.playing:
            screen.blit(self.action_anim.get_current_frame(), self.rect)
        else:
            screen.blit(self.default_sprite, self.rect)

    def draw_range(self, screen):
        self.range_circle.fill((0, 0, 0, 0))
        pygame.draw.circle(self.range_circle, (0, 0, 0, 125),
                           (self.range_circle.get_width() // 2, self.range_circle.get_height() // 2),
                           self.range * Cell.screen_size + Cell.screen_size // 2)
        screen.blit(self.range_circle, (self.rect.centerx - self.range_circle.get_width() / 2,
                                        self.rect.centery - self.range_circle.get_height() / 2))

    def place(self, cell):
        if cell is None:
            return
        if not cell.buildable:
            if self.last_cell is not None:
                self.place(self.last_cell)
        else:
            self.rect.center = (cell.get_screen_x(), cell.get_screen_y())
            self.attach(cell)
            self.state_context.game_var.level.gold -= self.cost

    def pickup(self):
        self.last_cell = self.cell
        self.detach()

    def detach(self):
        if self.cell is not None:
            self.cell.tower = None
            self.cell = None

    def attach(self, cell):
        if cell is not None:
            self.cell = cell
            self.cell.tower = self
            self.last_cell = self.cell

    def remove(self):
        self.detach()
        self.kill()

    def tick(self):
        self.screen_position = pygame.Vector2((self.rect.centerx, self.rect.centery))
        if self.cell is None:
            return
        self.tick_anim()
        if self.action_condition():
            if self.action_cooldown_ms_interactive <= 0:
                self.action()
                self.action_cooldown_ms_interactive = self.action_cooldown_ms

    def tick_anim(self):
        if self.action_anim is not None and self.action_anim.playing:
            self.action_anim.tick()

    def is_in_range(self, target):
        return (pygame.math.Vector2(self.cell.get_screen_x(), self.cell.get_screen_y()).
                distance_to((target.screen_position.x, target.screen_position.y))
                <= self.range * Cell.screen_size + Cell.screen_size / 2)

    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def action_condition(self):
        pass

    def return_to_last_cell(self):
        self.place(self.last_cell)
        self.attach(self.last_cell)
