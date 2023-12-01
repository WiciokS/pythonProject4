from abc import abstractmethod

from pygame.sprite import Sprite


class Projectile(Sprite):
    speed = 1
    damage = 1

    def __init__(self, state_context, default_sprite, flying_animation, target, source_position):
        Sprite.__init__(self)
        self.state_context = state_context
        self.flying_animation = flying_animation
        self.default_sprite = default_sprite
        self.rect = self.default_sprite.get_rect()
        self.target = target
        self.screen_position = source_position
        self.rect.center = (int(self.screen_position.x), int(self.screen_position.y))
        if self.flying_animation is not None:
            self.flying_animation.play()

    def tick(self):
        self.flying_animation.tick()
        self.move()
        self.rect.center = (int(self.screen_position.x), int(self.screen_position.y))

    def move(self):
        movement = self.target.screen_position - self.screen_position
        if movement.length() > self.speed:
            movement = movement.normalize() * self.speed
            self.screen_position += movement
        else:
            self.screen_position = self.target.screen_position
            self.hit()

    def draw(self, screen):
        if self.flying_animation is not None and self.flying_animation.playing:
            screen.blit(self.flying_animation.get_current_frame(), self.rect)
        else:
            screen.blit(self.default_sprite, self.rect)

    @abstractmethod
    def hit(self):
        pass

    def remove(self):
        self.state_context.game_var.level.projectiles.remove(self)
        del self

    def on_target(self):
        return self.target.screen_position == self.screen_position
