from abc import ABC, abstractmethod
from omg.structural.observer import Event
import arcade
import math
import os

ASSET_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "images")


# TODO: add source as the projectiles are emitted now
class Projectile(arcade.Sprite):
    def __init__(self, name, image_file, scale, damage, speed, init_px, init_py, angle):
        super().__init__(image_file, scale)
        self.image_file = image_file
        self.name = name
        self.damage = damage
        self.speed = speed
        # Set position + orientation
        self.center_x = init_px
        self.center_y = init_py
        self.angle = angle
        # Calculate the velocity of the projectile
        angle_rad = math.radians(angle + 90)  # Adjust the shooting angle accordingly
        self.change_x = self.speed * math.cos(angle_rad)
        self.change_y = self.speed * math.sin(angle_rad)


class ProjectileShotEvent(Event):
    """Event triggered when a projectile is shot."""

    def __init__(self, projectile: Projectile):
        """
        Parameters
        ----------
        projectile : Projectile
            The projectile that was shot.
        """
        super().__init__('projectile_shot')
        self.projectile = projectile


class ProjectileFactory(ABC):

    @classmethod
    @abstractmethod
    def create(cls, init_px: float, init_py: float, angle: float) -> Projectile:
        """Create and return a Projectile instance."""
        pass


class FireballFactory(ProjectileFactory):
    image_file = os.path.join(ASSET_DIR, "skills", "fireball.PNG")
    scale = 0.05
    damage = 25
    speed = 5

    @classmethod
    def create(cls, init_px, init_py, angle) -> Projectile:
        return Projectile(
            name=cls.__name__,
            image_file=cls.image_file,
            scale=cls.scale,
            damage=cls.damage,
            init_px=init_px,
            init_py=init_py,
            speed=cls.speed,
            angle=angle
        )


class IceShardFactory(ProjectileFactory):
    image_file = os.path.join(ASSET_DIR, "skills", "ice_shard.PNG")
    scale = 0.05
    damage = 15
    speed = 7

    @classmethod
    def create(cls, init_px, init_py, angle) -> Projectile:
        return Projectile(
            name=cls.__name__,
            image_file=cls.image_file,
            scale=cls.scale,
            damage=cls.damage,
            init_px=init_px,
            init_py=init_py,
            speed=cls.speed,
            angle=angle
        )
