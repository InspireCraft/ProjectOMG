import arcade
import math
import os

ASSET_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "images")


class Projectile(arcade.Sprite):
    def __init__(self, name, image_file, scale, damage, init_px, init_py, speed, angle):
        super().__init__(image_file, scale)
        self.name = name
        self.damage = damage
        self.speed = speed
        self.angle = angle
        self.center_x = init_px
        self.center_y = init_py
        # Calculate the velocity of the projectile
        angle_rad = math.radians(self.angle + 90)  # Adjust the shooting angle accordingly
        self.change_x = self.speed * math.cos(angle_rad)
        self.change_y = self.speed * math.sin(angle_rad)

