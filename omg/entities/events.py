from omg.structural.observer import Event
from omg.entities.projectile import Projectile


class PickupRequestEvent(Event):
    """Event triggered when an entity wants to pick up an item from the ground."""

    def __init__(self, entity, entity_pos_x, entity_pos_y, entity_pickup_radius):
        super().__init__("pickup_request")
        self.entity = entity
        self.entity_pos = (entity_pos_x, entity_pos_y)
        self.pickup_radius = entity_pickup_radius


class ProjectileShotEvent(Event):
    """Event triggered when a projectile is shot by an entity."""

    def __init__(self, projectile: Projectile):
        super().__init__("projectile_shot")
        self.projectile = projectile
