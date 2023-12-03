import pygame

from Animations.ArcherAttackAnimation import ArcherAttackAnimation
from Animations.MageAttackAnimation import MageAttackAnimation
from Maps.Base.Cell import Cell
from Projectiles.ArrowBulletProjectile import ArrowBulletProjectile
from Projectiles.MageBulletProjectile import MageBulletProjectile
from Towers.Base.Tower import Tower


class Archer(Tower):
    icon_path = 'Sprites/Archer/ArcherDefault.png'
    cost = 100
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
        if self.state_context.game_var.level.current_wave_index < len(self.state_context.game_var.level.waves):
            for enemy in self.state_context.game_var.level.waves[
                    self.state_context.game_var.level.current_wave_index].deployed_wave_enemies:
                if self.is_in_range(enemy):
                    if enemy not in self.possible_targets:
                        self.possible_targets.append(enemy)
                        continue
                else:
                    if enemy in self.possible_targets:
                        self.possible_targets.remove(enemy)

            # If target not in possible targets, remove it
            if self.target is not None:
                if self.target not in self.possible_targets:
                    self.target = None
                if self.target.health <= 0:
                    self.target = None

            # If there is no target, pick one
            if self.target is None:
                if len(self.possible_targets) > 0:
                    self.target = self.possible_targets[0]

            self.action_cooldown_ms_interactive -= self.state_context.app_var.app_clock.get_time()

            if self.target is not None:
                return True
        return False
