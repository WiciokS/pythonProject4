from abc import abstractmethod

from pygame.sprite import Sprite


class Button(Sprite):
    def __init__(self, default_sprite, hover_sprite=None, pressed_sprite=None):
        super().__init__()
        self.default_sprite = default_sprite
        self.hover_sprite = hover_sprite
        self.pressed_sprite = pressed_sprite
        self.rect = self.default_sprite.get_rect()

    @abstractmethod
    def action(self):
        pass
