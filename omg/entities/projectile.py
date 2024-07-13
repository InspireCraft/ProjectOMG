import arcade

class Projectile(arcade.Sprite):
    def __init__(self, name, image_file, scale, damage, speed):
        super().__init__(image_file, scale)
        self.name = name
        self.damage = damage
        self.speed = speed

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
