import pygame

from Maps.Base.Cell import Cell


class Tower(pygame.sprite.Sprite):
    def __init__(self, cell, default_sprite, action_anim=None, tower_range=1):
        pygame.sprite.Sprite.__init__(self)
        self.cell = cell
        self.range = tower_range
        self.last_cell = None
        self.default_sprite = default_sprite
        self.action_anim = action_anim
        self.rect = self.default_sprite.get_rect()
        if self.cell is not None:
            self.rect.center = (cell.get_screen_x(), cell.get_screen_y())
            self.cell.tower = self
        self.range_circle = pygame.Surface((self.range * Cell.screen_size + Cell.screen_size,
                                            self.range * Cell.screen_size + Cell.screen_size),
                                           pygame.SRCALPHA)

    def draw(self, screen):
        if self.action_anim is not None and self.action_anim.playing:
            screen.blit(self.action_anim.get_current_frame(), self.rect)
        else:
            screen.blit(self.default_sprite, self.rect)

    def draw_range(self, screen):
        self.range_circle.fill((0, 0, 0, 0))
        pygame.draw.circle(self.range_circle, (255, 255, 255, 50),
                           center=self.rect.center, radius=self.range_circle.get_rect().width // 2)
        screen.blit(self.range_circle, self.range_circle.get_rect(center=self.rect.center))

    def place(self, cell):
        if cell is None:
            return
        if not cell.buildable:
            if self.last_cell is not None:
                self.place(self.last_cell)
        else:
            self.rect.center = (cell.get_screen_x(), cell.get_screen_y())
            self.attach(cell)

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

    def remove(self):
        self.detach()
        self.kill()

    def return_to_last_cell(self):
        self.place(self.last_cell)
        self.attach(self.last_cell)
