import pygame

from Animations.MageBulletFlyingAnimation import MageBulletFlyingAnimation
from Projectiles.Base.Projectile import Projectile


class MageBulletProjectile(Projectile):
    speed = 5
    damage = 10

    def __init__(self, state_context, target, source_position):
        default_sprite = pygame.image.load(
            "Sprites/Projectile/MageBullet/Flying/MageBulletFlyingFrame1.png").convert_alpha()
        flying_animation = MageBulletFlyingAnimation()
        super().__init__(state_context, default_sprite, flying_animation, target, source_position)

    def hit(self):
        if self.target is not None:
            self.target.health -= self.damage
        self.remove()

