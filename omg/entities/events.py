import arcade
from omg.entities.items import ItemManager
from omg.structural.observer import Event
from omg.entities.projectile import Projectile


class PickupRequestEvent(Event):
    """Event triggered when an entity wants to pick up an item from the ground."""

    def __init__(
        self, entity, entity_pickup_sprite
    ):
        super().__init__("pickup_request")
        self.entity: ItemManager = entity
        self.entity_pickup_sprite: arcade.Sprite = entity_pickup_sprite


class ProjectileShotEvent(Event):
    """Event triggered when a projectile is shot by an entity."""

    def __init__(self, projectile: Projectile):
        super().__init__("projectile_shot")
        self.projectile = projectile
