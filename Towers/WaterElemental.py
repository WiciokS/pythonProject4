import pygame

from Animations.MageAttackAnimation import MageAttackAnimation
from Animations.WaterElementalAttackAnimation import WaterElementalAttackAnimation
from Maps.Base.Cell import Cell
from Projectiles.MageBulletProjectile import MageBulletProjectile
from Projectiles.WaterElementalBulletProjectile import WaterElementalBulletProjectile
from Towers.Base.Tower import Tower


class WaterElemental(Tower):
    icon_path = 'Sprites/WaterElemental/WaterElementalDefault.png'
    cost = 400
    action_cooldown_ms = 3000
    range = 1

    def __init__(self, state_context, cell=None):
        self.state_context = state_context
        self.default_sprite = pygame.image.load("Sprites/WaterElemental/WaterElementalDefault.png").convert_alpha()
        self.default_sprite = pygame.transform.scale(self.default_sprite, (Cell.screen_size, Cell.screen_size))
        self.action_anim = WaterElementalAttackAnimation()
        super().__init__(state_context, cell, self.default_sprite, self.action_anim)

    def action(self):
        self.action_anim.play()
        self.state_context.game_var.level.projectiles.append(
            WaterElementalBulletProjectile(self.state_context, self.target, self.screen_position))

    def action_condition(self):
        self.pick_enemy_target_in_range()
        self.action_cooldown_ms_interactive -= self.state_context.app_var.app_clock.get_time()
        if self.target is not None:
            return True
        else:
            return False
