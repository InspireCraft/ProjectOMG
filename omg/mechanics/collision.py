import arcade
from typing import List
from entities.obstacle import Obstacle
from entities.projectile import Projectile

def handle_obstacle_collisions(sprite, obstacles):
    # Check for collision with obstacles
    if arcade.check_for_collision_with_list(sprite, obstacles):
        sprite.center_x -= sprite.change_x
        sprite.center_y -= sprite.change_y

def handle_screen_boundary_collision(sprite, screen_width, screen_height):
    # Check for collision with screen boundaries
    if sprite.left < 0:
        sprite.left = 0
    if sprite.right > screen_width:
        sprite.right = screen_width
    if sprite.bottom < 0:
        sprite.bottom = 0
    if sprite.top > screen_height:
        sprite.top = screen_height

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
