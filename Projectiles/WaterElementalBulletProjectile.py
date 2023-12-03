import pygame

from Animations.MageBulletFlyingAnimation import MageBulletFlyingAnimation
from Animations.WaterElementalBulletFlyingAnimation import WaterElementalBulletFlyingAnimation
from Maps.Base.Cell import Cell
from Maps.Base.Map import Map
from Projectiles.Base.Projectile import Projectile


class WaterElementalBulletProjectile(Projectile):
    speed = 0.35
    damage = 100

    def __init__(self, state_context, target, source_position):
        default_sprite = pygame.image.load(
            "Sprites/Projectile/WaterElementalBullet/Flying/WaterElementalBulletFlyingFrame1.png").convert_alpha()
        flying_animation = WaterElementalBulletFlyingAnimation()
        super().__init__(state_context, default_sprite, flying_animation, target, source_position, homing=False)

    def hit(self):
        for enemy in self.state_context.game_var.level.waves[
                self.state_context.game_var.level.current_wave_index].deployed_wave_enemies:
            if self.is_in_range(enemy):
                enemy_cell_position = self.state_context.game_var.level.map.convert_screen_coordinates_to_cells(
                    enemy.screen_position)[0]
                projectile_cell_position = self.state_context.game_var.level.map.convert_screen_coordinates_to_cells(
                    self.screen_position)[0]
                dir_to_enemy_x = (self.state_context.game_var.level.map.convert_cells_to_screen_coordinates(
                    [enemy_cell_position])[0][0]
                                  - self.state_context.game_var.level.map.convert_cells_to_screen_coordinates(
                            [projectile_cell_position])[0][0])
                dir_to_enemy_y = (self.state_context.game_var.level.map.convert_cells_to_screen_coordinates(
                    [enemy_cell_position])[0][1]
                                  - self.state_context.game_var.level.map.convert_cells_to_screen_coordinates(
                            [projectile_cell_position])[0][1])

                push_x = 0
                push_y = 0

                if dir_to_enemy_x > 0:
                    dir_to_enemy_x = 1
                elif dir_to_enemy_x < 0:
                    dir_to_enemy_x = -1
                if dir_to_enemy_y > 0:
                    dir_to_enemy_y = 1
                elif dir_to_enemy_y < 0:
                    dir_to_enemy_y = -1

                if dir_to_enemy_x != 0:
                    push_x = dir_to_enemy_x * Cell.screen_size
                if dir_to_enemy_y == dir_to_enemy_y != 0:
                    push_y = dir_to_enemy_y * Cell.screen_size

                enemy.push(push_x, push_y)
                enemy.health -= self.damage

        self.remove()

    def is_in_range(self, target):
        return (pygame.math.Vector2(self.screen_position.x, self.screen_position.y).
                distance_to((target.screen_position.x, target.screen_position.y))
                <= 2 * Cell.screen_size + Cell.screen_size / 2)
