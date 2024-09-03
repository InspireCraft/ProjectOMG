from abc import ABC, abstractmethod
from typing import Dict
import arcade
import math
import os
import json

JSON_DIR = os.path.join(os.path.dirname(__file__), "CraftedSkills.JSON")

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

with open(JSON_DIR, "r") as file:
    crafted_skill_dictionary: Dict[str,Dict] = json.load(file)

class CraftingSkillFactory(ProjectileFactory):
    """Class to combine elements to craft a skill."""
    
    @classmethod
    def _set_skill_attributes(cls, skill_name: str):
        """Set the class attributes based on the skill_name."""
        cls.image_file = crafted_skill_dictionary[skill_name]["image_file"]
        cls.scale = crafted_skill_dictionary[skill_name]["scale"]
        cls.damage = crafted_skill_dictionary[skill_name]["damage"]
        cls.speed = crafted_skill_dictionary[skill_name]["speed"]
        cls.mana_cost = crafted_skill_dictionary[skill_name]["mana_cost"]
    
    image_file = None
    scale = None
    damage = None
    speed = None
    mana_cost = None
