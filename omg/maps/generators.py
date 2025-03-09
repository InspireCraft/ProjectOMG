from math import ceil
import random
from typing import Callable, List

import arcade


class SpriteGenerator():
    """Class to generate sprites in the scene."""

    @staticmethod
    def generate_sprites_in_area(
        area_size: tuple[int, int],
        area_left_bottom: tuple[int, int] = (0, 0),
        count: int = 0,
        no_overlap_sprites: List[arcade.SpriteList] = [],
        min_size=10,
        max_size=100,
        sprite_init_fn: Callable[[], arcade.Sprite] = lambda: arcade.SpriteSolidColor(
            width=1, height=1, color=arcade.color.BABY_BLUE
        ),
        random_size: bool = False,
        random_position: bool = True,
        random_angle: bool = True,
    ):
        """Generate sprites in an area."""
        sprites = arcade.SpriteList()
        for i in range(count):
            sprite = sprite_init_fn()

            if random_size:
                sprite.width = random.randint(min_size, max_size)
                sprite.height = random.randint(min_size, max_size)
            else:
                sprite.width = max(min(sprite.width, max_size), min_size)
                sprite.height = max(min(sprite.height, max_size), min_size)

            if random_position:
                area_left, area_bottom = area_left_bottom
                area_right = area_left + area_size[0]
                area_top = area_bottom + area_size[1]

                x_min = area_left
                x_max = int(ceil(area_right - sprite.width))
                x = random.randint(x_min, x_max)
                sprite.center_x = x

                y_min = area_bottom
                y_max = int(ceil(area_top - sprite.height))
                y = random.randint(y_min, y_max)
                sprite.center_y = y

            if random_angle:
                sprite.angle = random.randint(0, 360)

            # Check if sprite collides with other sprites in the scene,
            counter = 0
            max_counter = 100
            is_placeable = False
            while counter < max_counter:
                collided_sprites = _collides_with_lists(sprite, no_overlap_sprites)
                if len(collided_sprites) == 0:
                    is_placeable = True
                    break

                # If collides, then put it into the closest possible place
                # Correct based on the direction vector which shows the closest
                # direction to the scene sprite and move in the opposite way
                closest_collided = arcade.get_closest_sprite(sprite, collided_sprites)[0]
                direction_away = (
                    sprite.center_x - closest_collided.center_x,
                    sprite.center_y - closest_collided.center_y
                )
                sprite.center_x += direction_away[0]
                sprite.center_y += direction_away[1]

                # Update loop counter
                counter += 1
            else:
                # Loop ended without triggering 'break', meaning that the
                # sprite could not be placed in the scene without overlapping
                # with other sprites.
                is_placeable = False

            if is_placeable:
                sprites.append(sprite)
        return sprites


def _collides_with_lists(sprite: arcade.Sprite, sprite_lists: List[arcade.SpriteList]):
    """Check if sprite collides with the list of given SpriteLists."""
    collided_sprites = arcade.SpriteList()
    for sprite_list in sprite_lists:
        collided_sprites.extend(sprite.collides_with_list(sprite_list))
    return collided_sprites
