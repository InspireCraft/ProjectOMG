from abc import ABC, abstractmethod
from typing import Dict
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
    """Abstract base class for projectile factories."""

    @property
    @abstractmethod
    def image_file(self) -> str:
        pass

    @property
    @abstractmethod
    def scale(self) -> float:
        pass

    @property
    @abstractmethod
    def damage(self) -> float:
        pass

    @property
    @abstractmethod
    def speed(self) -> float:
        pass

    @property
    @abstractmethod
    def mana_cost(self) -> float:
        pass

    @classmethod
    def create(cls, init_px, init_py, angle) -> Projectile:
        """Create a projectile with class-specific attributes."""
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

my_dict = {
    "FireFire":{
        "image_file": os.path.join(ASSET_DIR, "skills", "FireFire.PNG"),
        "scale": 0.05,
        "damage": 15,
        "speed": 7,
        "mana_cost": 20
    }
}

class CraftingSkillFactory(ProjectileFactory):
    """Class to combine elements to craft a skill."""
    
    @classmethod
    def _set_skill_attributes(cls, skill_name: str):
        """Set the class attributes based on the skill_name."""
        cls.image_file = my_dict[skill_name]["image_file"]
        cls.scale = my_dict[skill_name]["scale"]
        cls.damage = my_dict[skill_name]["damage"]
        cls.speed = my_dict[skill_name]["speed"]
        cls.mana_cost = my_dict[skill_name]["mana_cost"]
    
    image_file = None
    scale = None
    damage = None
    speed = None
    mana_cost = None
    

class IceFireFactory(ProjectileFactory):
    """Convenience class to create Ice-spear Projectile."""

    image_file = os.path.join(ASSET_DIR, "skills", "IceFire.PNG")
    scale = 0.05
    damage = 15
    speed = 7
    mana_cost = 20


class IceIceFactory(ProjectileFactory):
    """Convenience class to create IceShard Projectile."""

    image_file = os.path.join(ASSET_DIR, "skills", "IceIce.PNG")
    scale = 0.05
    damage = 15
    speed = 7
    mana_cost = 20


class FireIceFactory(ProjectileFactory):
    """Convenience class to create Cold-fireball Projectile."""

    image_file = os.path.join(ASSET_DIR, "skills", "FireIce.PNG")
    scale = 0.05
    damage = 15
    speed = 7
    mana_cost = 20


class FireFireFactory(ProjectileFactory):
    """Convenience class to create Fireball Projectile."""

    image_file = os.path.join(ASSET_DIR, "skills", "FireFire.PNG")
    scale = 0.05
    damage = 15
    speed = 7
    mana_cost = 20


COMBINED_ELEMENT_DICTIONARY: Dict[str, ProjectileFactory] = {
    "FireFire": FireFireFactory(),
    "FireIce": FireIceFactory(),
    "IceFire": IceFireFactory(),
    "IceIce": IceIceFactory(),
}
