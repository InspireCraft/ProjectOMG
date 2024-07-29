import arcade
from typing import List
from entities.obstacle import Obstacle
from entities.projectile import Projectile


def handle_projectile_collisions(
    projectiles: List[Projectile],
    obstacles: List[Obstacle]
):
    for projectile in projectiles:
        hit_list: List[Obstacle] = arcade.check_for_collision_with_list(
            projectile,
            obstacles
        )
        for obstacle in hit_list:
            obstacle.take_damage(projectile.damage)
            projectile.kill()
