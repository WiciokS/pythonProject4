import pygame

from Animations.MageAttackAnimation import MageAttackAnimation
from Maps.Base.Cell import Cell
from Projectiles.MageBulletProjectile import MageBulletProjectile
from Towers.Base.Tower import Tower


class Mage(Tower):
    range = 2
    action_cooldown_ms = 1000

    def __init__(self, state_context, cell=None):
        self.state_context = state_context
        self.default_sprite = pygame.image.load("Sprites/Mage/MageDefault.png").convert_alpha()
        self.default_sprite = pygame.transform.scale(self.default_sprite, (Cell.screen_size, Cell.screen_size))
        self.action_anim = MageAttackAnimation()
        super().__init__(state_context, cell, self.default_sprite, self.action_anim)

    def action_condition(self):
        # Go through each enemy in range and see if they are in target list
        for enemy in self.state_context.game_var.level.deployed_enemies:
            if self.is_in_range(enemy):
                if enemy not in self.possible_targets:
                    self.possible_targets.append(enemy)
                    continue
            if not self.is_in_range(enemy):
                if enemy in self.possible_targets:
                    self.possible_targets.remove(enemy)
                    if self.target == enemy:
                        self.target = None
        # If there is no target, pick one
        if self.target is None:
            if len(self.possible_targets) > 0:
                self.target = self.possible_targets[0]

        self.action_cooldown_ms_interactive -= self.state_context.game_var.level.clock.get_time()

        if self.target is not None:
            return True
        return False

    def action(self):
        self.action_anim.play()
        self.state_context.game_var.level.projectiles.append(MageBulletProjectile(self.target, self.screen_position))

