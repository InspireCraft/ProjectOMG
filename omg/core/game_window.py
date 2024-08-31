import arcade
import os

from omg.entities.items import Pickupable
from omg.entities.player import Player
from omg.entities.obstacle import Obstacle
from omg.entities.projectile import (
    FireElementFactory,
    IceElementFactory,
)
from omg.mechanics.collision import handle_projectile_collisions
from omg.mechanics.physics import PhysicsEngineBoundary
from omg.structural.observer import Observer
from omg.entities.events import PickupRequestEvent, ProjectileShotEvent


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "2D Shooter RPG"

ASSET_DIR = os.path.join(
    os.path.join(os.path.dirname(__file__), ".."), "assets", "images"
)

COIN_IMAGE_PATH = ":resources:images/items/coinGold.png"


class GameWindow(arcade.Window):
    """Main game window."""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.observer: Observer = None
        self.player: Player = None
        self.obstacles: arcade.SpriteList = None
        self.pickupables: arcade.SpriteList = (
            None  # items that can be pickedup from the ground
        )
        self.skill_slot_d: arcade.Sprite = None  # Skill slot D
        self.skill_slot_f: arcade.Sprite = None  # SKill slot F
        self.projectiles = None
        self.physics_engine = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.icon_scale = 0.1
        self.icon_margin_x = 10
        self.icon_margin_y = 75
        self.icon_size = 64

    def setup(self):
        """Reset the game state."""
        self.observer = Observer()
        self.observer.register_handler("projectile_shot", self._on_projectile_shot)
        self.observer.register_handler("pickup_request", self._on_pickup_request)
        self.player = Player(
            name="Hero",
            char_class="Wizard",
            image_file=os.path.join(ASSET_DIR, "characters", "wizard_td2.PNG"),
            scale=0.2,
            initial_angle=0,
        )
        self.player.add_observer(self.observer)

        # Create obstacles
        self.obstacles = arcade.SpriteList()
        self.pickupables = arcade.SpriteList(use_spatial_hash=True)
        self.projectiles = arcade.SpriteList()
        obstacle_image = os.path.join(ASSET_DIR, "obstacles", "obstacle.png")
        obstacle = Obstacle(obstacle_image, 0.2, health=50)
        obstacle.center_x = 400
        obstacle.center_y = 300
        self.obstacles.append(obstacle)
        
        # Create skill slots
        # Skill slot D
        scale_factor_d = 0.4
        skill_slot_d_img = os.path.join(ASSET_DIR, "skill_slots_d_f", "D.png")
        self.skill_slot_d = arcade.Sprite(skill_slot_d_img, scale=scale_factor_d)
        self.skill_slot_d.center_x = self.skill_slot_d.width // 2
        self.skill_slot_d.center_y = self.skill_slot_d.height // 2
        
        # Skill slot F
        scale_factor_f = 0.4
        skill_slot_f_img = os.path.join(ASSET_DIR, "skill_slots_d_f", "F.png")
        self.skill_slot_f = arcade.Sprite(skill_slot_f_img, scale=scale_factor_f)
        self.skill_slot_f.center_x = self.skill_slot_d.center_x + self.skill_slot_f.width
        self.skill_slot_f.center_y = self.skill_slot_f.height // 2
        
        

        self.physics_engine = PhysicsEngineBoundary(
            player_sprite=self.player,
            walls=self.obstacles,
            screen_width=SCREEN_WIDTH,
            screen_height=SCREEN_HEIGHT,
        )
        # Add projectile types
        self.pickupables.append(
            Pickupable(COIN_IMAGE_PATH, 0.5, FireElementFactory, 150, 10)
        )
        self.pickupables.append(
            Pickupable(COIN_IMAGE_PATH, 0.5, IceElementFactory, 250, 20)
        )
        self.pickupables.append(
            Pickupable(COIN_IMAGE_PATH, 0.5, FireElementFactory, 250, 120)
        )

    @property
    def skill_icons(self):
        """Define self.skill_icons."""
        # TODO: refactor skill_icons logic if causes a performance bottleneck
        # For example "skill_acquired event" can trigger an update when necessary
        if self.player:
            return [
                arcade.load_texture(projectile_type.image_file)
                for projectile_type in self.player.element
            ]
        else:
            return None

    def _load_skill_icons(self):
        for projectile_type in self.player.element:
            icon_texture = arcade.load_texture(projectile_type.image_file)
            self.skill_icons.append(icon_texture)

    def on_draw(self):
        """Drawing code."""
        arcade.start_render()
        self.player.draw()
        self.obstacles.draw()
        self.projectiles.draw()
        self.pickupables.draw()
        self._draw_ui()

    def update(self, delta_time):
        """Main update window."""
        self.player.update(self.mouse_x, self.mouse_y, delta_time)
        self.obstacles.update()
        self.physics_engine.update()
        self.projectiles.update()
        handle_projectile_collisions(self.projectiles, self.obstacles)

    def _on_projectile_shot(self, event: ProjectileShotEvent):
        self.projectiles.append(event.projectile)

    def _on_pickup_request(self, event: PickupRequestEvent):
        """Handles pickup request of an entity.

        Handling logic:
        1) Checks pickupables in the environment with the current posiiton of the entity
           requesting a pickup.
        2) Pickup area is indicated with the hitbox of the event.entity_pickup_sprite
           so collision check can be used.
        3) Out of all the collisions, let the entity pick up the closest object.
        4) Remove the picked up item from the ground.
        """
        collided_sprites: list[Pickupable] = arcade.check_for_collision_with_list(
            event.entity_pickup_sprite, self.pickupables
        )
        if len(collided_sprites) >= 1:
            # Item is at pick up range
            closes_pickupable: Pickupable = arcade.get_closest_sprite(
                event.entity_pickup_sprite, collided_sprites
            )[0]
            item_to_add = collided_sprites[0]
            item_manager = event.entity
            item_manager.add_item(closes_pickupable.item)
            # remove reference to the pickupables list
            item_to_add.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        """Key press logic."""
        # Delegate the input
        self.player.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        """Key release logic."""
        # Delegate the input
        self.player.on_key_release(key, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        """Adds mouse functionality to the game."""
        self.mouse_x = x
        self.mouse_y = y

    def _draw_ui(self):
        # Draw picked up skills to top left corner
        for i, icon in enumerate(self.skill_icons):
            x = self.icon_margin_x + i * (self.icon_size + self.icon_margin_x)
            y = SCREEN_HEIGHT - self.icon_margin_y
            if i == self.player.element.get_current_index():
                arcade.draw_rectangle_outline(
                    x + self.icon_size // 2,
                    y + self.icon_size // 2,
                    self.icon_size,
                    self.icon_size,
                    arcade.color.RED,
                    border_width=3,
                )
            arcade.draw_texture_rectangle(
                x + self.icon_size // 2,
                y + self.icon_size // 2,
                self.icon_size,
                self.icon_size,
                icon,
            )
        
        # Draw combined skill icons
        if self.player.skills_in_slots_d_f[0] != None:
            scale_factor_d = 0.3
            skill_d_img = os.path.join(ASSET_DIR, "skills", f"{self.player.skills_in_slots_d_f[0]}.png")
            skill_d = arcade.Sprite(skill_d_img, scale=scale_factor_d)
            skill_d.center_x = skill_d.width // 2
            skill_d.center_y = skill_d.height // 2
            skill_d.draw()
           
        if self.player.skills_in_slots_d_f[1] != None:
            scale_factor_f = 0.3
            skill_f_img = os.path.join(ASSET_DIR, "skills", f"{self.player.skills_in_slots_d_f[1]}.png")
            skill_f = arcade.Sprite(skill_f_img, scale=scale_factor_f)
            skill_f.center_x = skill_f.width // 2 + skill_f.width
            skill_f.center_y = skill_f.height // 2
            skill_f.draw()
            
                
        # Draw usable skill slots to bottom left corner
        self.skill_slot_d.draw()
        self.skill_slot_f.draw()


def main():
    """Main application code."""
    window = GameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
