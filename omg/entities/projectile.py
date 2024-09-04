from abc import ABC, abstractmethod
from typing import Dict
import arcade
import math
import os
import json

CRAFTED_SKILLS_JSON_DIR = os.path.join(os.path.dirname(__file__), "CraftedSkills.JSON")


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

    def __init__(self) -> None:
        self.name: str = None
        self.image_file: str = None
        self.scale: float = None
        self.damage: float = None
        self.speed: float = None
        self.mana_cost: float = None

    def create(self, init_px, init_py, angle) -> Projectile:
        """Create a projectile with class-specific attributes."""
        return Projectile(
            name=self.name,
            image_file=self.image_file,
            scale=self.scale,
            damage=self.damage,
            init_px=init_px,
            init_py=init_py,
            speed=self.speed,
            angle=angle,
        )


with open(CRAFTED_SKILLS_JSON_DIR, "r") as file:
    crafted_skill_dictionary: Dict[str, Dict] = json.load(file)


class SkillFactory(ProjectileFactory):
    """Class to combine elements to craft a skill."""
    
    def __init__(self) -> None:
        self.name = None
        self.image_file = None
        self.scale = None
        self.damage = None
        self.speed = None
        self.mana_cost = None
        
    def set_skill_attributes(self, skill_name: str):
        """Set the class attributes based on the skill_name."""
        self.name = skill_name
        self.image_file = crafted_skill_dictionary[skill_name]["image_file"]
        self.scale = crafted_skill_dictionary[skill_name]["scale"]
        self.damage = crafted_skill_dictionary[skill_name]["damage"]
        self.speed = crafted_skill_dictionary[skill_name]["speed"]
        self.mana_cost = crafted_skill_dictionary[skill_name]["mana_cost"]
