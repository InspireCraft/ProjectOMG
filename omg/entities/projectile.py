from abc import ABC, abstractmethod
import arcade
import math
import os

ASSET_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "images")


# TODO: add source as the projectiles are emitted now
class Projectile(arcade.Sprite):
    """Projectile logic."""

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


class ProjectileFactory(ABC):
    """Abstract class for Projectile creating factories."""

    image_file: str

    @classmethod
    @abstractmethod
    def create(cls, init_px: float, init_py: float, angle: float) -> Projectile:
        """Create and return a Projectile instance."""
        pass

class FireElementFactory(ProjectileFactory):
    """Convenience class to create Fireball Projectile."""

    image_file = os.path.join(ASSET_DIR, "skills", "elements", "fire.PNG")
    scale = 0.05
    damage = 25
    speed = 5

    @classmethod
    def create(cls, init_px, init_py, angle) -> Projectile:
        """Create a Fireball projectile."""
        return Projectile(
            name=cls.__name__,
            image_file=cls.image_file,
            scale=cls.scale,
            damage=cls.damage,
            init_px=init_px,
            init_py=init_py,
            speed=cls.speed,
            angle=angle,
        )


class IceElementFactory(ProjectileFactory):
    """Convenience class to create IceShard Projectile."""

    image_file = os.path.join(ASSET_DIR, "skills", "elements", "ice.PNG")
    scale = 0.05
    damage = 15
    speed = 7

    @classmethod
    def create(cls, init_px, init_py, angle) -> Projectile:
        """Create an IceShard projectile."""
        return Projectile(
            name=cls.__name__,
            image_file=cls.image_file,
            scale=cls.scale,
            damage=cls.damage,
            init_px=init_px,
            init_py=init_py,
            speed=cls.speed,
            angle=angle,
        )
        
class IceFireFactory(ProjectileFactory):
    """Convenience class to create IceShard Projectile."""

    image_file = os.path.join(ASSET_DIR, "skills", "IceFire.PNG")
    scale = 0.05
    damage = 15
    speed = 7

    @classmethod
    def create(cls, init_px, init_py, angle) -> Projectile:
        """Create an IceShard projectile."""
        return Projectile(
            name=cls.__name__,
            image_file=cls.image_file,
            scale=cls.scale,
            damage=cls.damage,
            init_px=init_px,
            init_py=init_py,
            speed=cls.speed,
            angle=angle,
        )     

class IceIceFactory(ProjectileFactory):
    """Convenience class to create IceShard Projectile."""

    image_file = os.path.join(ASSET_DIR, "skills", "IceIce.PNG")
    scale = 0.05
    damage = 15
    speed = 7

    @classmethod
    def create(cls, init_px, init_py, angle) -> Projectile:
        """Create an IceShard projectile."""
        return Projectile(
            name=cls.__name__,
            image_file=cls.image_file,
            scale=cls.scale,
            damage=cls.damage,
            init_px=init_px,
            init_py=init_py,
            speed=cls.speed,
            angle=angle,
        )     

        
class FireIceFactory(ProjectileFactory):
    """Convenience class to create IceShard Projectile."""

    image_file = os.path.join(ASSET_DIR, "skills", "FireIce.PNG")
    scale = 0.05
    damage = 15
    speed = 7

    @classmethod
    def create(cls, init_px, init_py, angle) -> Projectile:
        """Create an IceShard projectile."""
        return Projectile(
            name=cls.__name__,
            image_file=cls.image_file,
            scale=cls.scale,
            damage=cls.damage,
            init_px=init_px,
            init_py=init_py,
            speed=cls.speed,
            angle=angle,
        )

class FireFireFactory(ProjectileFactory):
    """Convenience class to create IceShard Projectile."""

    image_file = os.path.join(ASSET_DIR, "skills", "FireFire.PNG")
    scale = 0.05
    damage = 15
    speed = 7

    @classmethod
    def create(cls, init_px, init_py, angle) -> Projectile:
        """Create an IceShard projectile."""
        return Projectile(
            name=cls.__name__,
            image_file=cls.image_file,
            scale=cls.scale,
            damage=cls.damage,
            init_px=init_px,
            init_py=init_py,
            speed=cls.speed,
            angle=angle,
        )
        
COMBINED_ELEMENT_DICTIONARY = {
            "FireFire" : FireFireFactory(),
            "FireIce"  : FireIceFactory(),
            "IceFire"  : IceFireFactory(),
            "IceIce"   : IceIceFactory(),
        }