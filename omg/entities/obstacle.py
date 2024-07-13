import arcade

class Obstacle(arcade.Sprite):
    def __init__(self, image_file, scale, health):
        super().__init__(image_file, scale)
        self.health = health

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
