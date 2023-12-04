import pygame

from Animations.ArcherAttackAnimation import ArcherAttackAnimation
from Animations.MageAttackAnimation import MageAttackAnimation
from Maps.Base.Cell import Cell
from Projectiles.ArrowBulletProjectile import ArrowBulletProjectile
from Projectiles.MageBulletProjectile import MageBulletProjectile
from Towers.Base.Tower import Tower


class Archer(Tower):
    icon_path = 'Sprites/Archer/ArcherDefault.png'
    cost = 300
    action_cooldown_ms = 300
    range = 5

    def __init__(self, state_context, cell=None):
        self.state_context = state_context
        self.default_sprite = pygame.image.load("Sprites/Archer/ArcherDefault.png").convert_alpha()
        self.default_sprite = pygame.transform.scale(self.default_sprite, (Cell.screen_size, Cell.screen_size))
        self.action_anim = ArcherAttackAnimation()
        super().__init__(state_context, cell, self.default_sprite, self.action_anim)

    def action(self):
        self.action_anim.play()
        self.state_context.game_var.level.projectiles.append(
            ArrowBulletProjectile(self.state_context, self.target, self.screen_position))

    def action_condition(self):
        self.pick_enemy_target_in_range()
        self.action_cooldown_ms_interactive -= self.state_context.app_var.app_clock.get_time()
        if self.target is not None:
            return True
        else:
            return False
