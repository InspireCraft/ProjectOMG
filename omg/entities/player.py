import arcade
import math
from entities.projectile import Projectile
from mechanics.collision import handle_obstacle_collisions, handle_screen_boundary_collision

class Player(arcade.Sprite):
    def __init__(self, name, char_class, image_file, scale, initial_angle=0):
        super().__init__(image_file, scale)
        self.name = name
        self.char_class = char_class
        self.center_x = 100
        self.center_y = 100
        self.change_x = 0
        self.change_y = 0
        self.projectiles = arcade.SpriteList()
        self.angle = initial_angle  # Set initial angle here

    def update(self, mouse_x, mouse_y, obstacles, screen_width, screen_height):
        self.center_x += self.change_x
        self.center_y += self.change_y
        handle_obstacle_collisions(self, obstacles)
        handle_screen_boundary_collision(self, screen_width, screen_height)
        self.projectiles.update()
        self.face_mouse(mouse_x, mouse_y)

    def face_mouse(self, mouse_x, mouse_y):
        # Adjust the angle by 90 degrees to ensure the top of the sprite faces the mouse
        self.angle = math.degrees(math.atan2(mouse_y - self.center_y, mouse_x - self.center_x)) - 90

    def shoot(self, projectile_image, scale, damage, speed):
        projectile = Projectile(name="Basic Shot", image_file=projectile_image, scale=scale, damage=damage, speed=speed)
        projectile.center_x = self.center_x
        projectile.center_y = self.center_y
        angle_rad = math.radians(self.angle + 90)  # Adjust the shooting angle accordingly
        projectile.change_x = speed * math.cos(angle_rad)
        projectile.change_y = speed * math.sin(angle_rad)
        self.projectiles.append(projectile)

    def draw(self):
        super().draw()
        self.projectiles.draw()
