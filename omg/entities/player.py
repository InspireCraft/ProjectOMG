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

        # Health
        self.max_health = 100
        self.current_health = 100

        # Mana
        self.max_mana = 100
        self.current_mana = 100
        self.mana_regen_rate = 5  # Mana regenerated per second
        self.mana_regen_cooldown = 0

        # Default movement keys
        self.key_forward = arcade.key.W
        self.key_backward = arcade.key.S
        self.key_left = arcade.key.A
        self.key_right = arcade.key.D

        # Projectile types
        self.projectile_types = []
        self.current_projectile_index = 0

    def update(self, mouse_x, mouse_y, obstacles, screen_width, screen_height, delta_time):
        self.update_position()
        handle_obstacle_collisions(self, obstacles)
        handle_screen_boundary_collision(self, screen_width, screen_height)
        self.projectiles.update()
        self.face_mouse(mouse_x, mouse_y)
        self.regenerate_mana(delta_time)

    def update_position(self):
        forward_x, forward_y = self.calculate_movement_vector(self.angle + 90)
        right_x, right_y = self.calculate_movement_vector(self.angle)

        self.center_x += self.change_x * forward_x + self.change_y * right_x
        self.center_y += self.change_x * forward_y + self.change_y * right_y

    def calculate_movement_vector(self, angle):
        radian_angle = math.radians(angle)
        return math.cos(radian_angle), math.sin(radian_angle)

    def face_mouse(self, mouse_x, mouse_y):
        # Adjust the angle by 90 degrees to ensure the top of the sprite faces the mouse
        self.angle = math.degrees(math.atan2(mouse_y - self.center_y, mouse_x - self.center_x)) - 90

    def shoot(self):
        if not self.projectile_types or self.current_mana < 20:
            return
        
        self.current_mana -= 20
        projectile_info = self.projectile_types[self.current_projectile_index]
        projectile = Projectile(
            name=projectile_info['name'],
            image_file=projectile_info['image_file'],
            scale=projectile_info['scale'],
            damage=projectile_info['damage'],
            speed=projectile_info['speed']
        )
        projectile.center_x = self.center_x
        projectile.center_y = self.center_y
        angle_rad = math.radians(self.angle + 90)  # Adjust the shooting angle accordingly
        projectile.change_x = projectile_info['speed'] * math.cos(angle_rad)
        projectile.change_y = projectile_info['speed'] * math.sin(angle_rad)
        self.projectiles.append(projectile)

    def regenerate_mana(self, delta_time):
        self.mana_regen_cooldown += delta_time
        if self.mana_regen_cooldown >= 1:
            self.current_mana += self.mana_regen_rate
            if self.current_mana > self.max_mana:
                self.current_mana = self.max_mana
            self.mana_regen_cooldown = 0

    def add_projectile_type(self, name, image_file, scale, damage, speed):
        self.projectile_types.append({
            'name': name,
            'image_file': image_file,
            'scale': scale,
            'damage': damage,
            'speed': speed
        })

    def select_projectile(self, index):
        if 0 <= index < len(self.projectile_types):
            self.current_projectile_index = index

    def set_movement_keys(self, forward, backward, left, right):
        self.key_forward = forward
        self.key_backward = backward
        self.key_left = left
        self.key_right = right

    def draw(self):
        super().draw()
        self.projectiles.draw()
        self.draw_health_bar()
        self.draw_mana_bar()

    def draw_health_bar(self):
        health_bar_width = 50
        health_bar_height = 5
        health_bar_x = self.center_x
        health_bar_y = self.center_y + self.height / 2 + 10
        arcade.draw_rectangle_filled(
            health_bar_x,
            health_bar_y,
            health_bar_width,
            health_bar_height,
            arcade.color.RED
        )
        current_health_width = health_bar_width * (self.current_health / self.max_health)
        arcade.draw_rectangle_filled(
            health_bar_x - (health_bar_width - current_health_width) / 2,
            health_bar_y,
            current_health_width,
            health_bar_height,
            arcade.color.GREEN
        )

    def draw_mana_bar(self):
        mana_bar_width = 50
        mana_bar_height = 5
        mana_bar_x = self.center_x
        mana_bar_y = self.center_y + self.height / 2 + 2  # Slightly below the health bar
        arcade.draw_rectangle_filled(
            mana_bar_x,
            mana_bar_y,
            mana_bar_width,
            mana_bar_height,
            arcade.color.DARK_BLUE
        )
        current_mana_width = mana_bar_width * (self.current_mana / self.max_mana)
        arcade.draw_rectangle_filled(
            mana_bar_x - (mana_bar_width - current_mana_width) / 2,
            mana_bar_y,
            current_mana_width,
            mana_bar_height,
            arcade.color.LIGHT_BLUE
        )
