import pygame

from Animations.MageBulletFlyingAnimation import MageBulletFlyingAnimation
from Maps.Base.Cell import Cell
from Projectiles.Base.Projectile import Projectile


class MageBulletProjectile(Projectile):
    speed = 5
    damage = 10

    def __init__(self, state_context, target, source_position):
        sprite = pygame.image.load(
            "Sprites/Projectile/MageBullet/Flying/MageBulletFlyingFrame1.png").convert_alpha()
        default_sprite = pygame.transform.scale(sprite, (Cell.screen_size, Cell.screen_size))
        flying_animation = MageBulletFlyingAnimation()
        super().__init__(state_context, default_sprite, flying_animation, target, source_position)

    def hit(self):
        if self.target is not None:
            self.target.health -= self.damage
        self.remove()

