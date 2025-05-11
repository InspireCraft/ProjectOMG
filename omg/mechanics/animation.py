import os
from typing import Tuple

import arcade


class Animation():
    """Class to represent a single type of animation."""

    def __init__(self, path: str, action: str):
        self._my_hidden_dict = dict[str, list[list, int, int]]
        self.textures: dict[str, list] = {}
        self.counters: dict[str, int] = {}
        self._number_of_textures: dict[str, int] = {}

        directions = ['up', 'down', 'left', 'right']
        for direction in directions:
            self.textures[direction] = []
            self.counters[direction] = 0

            for file_name in os.listdir(path):
                # print(file_name)
                if file_name.startswith(f'{action}_{direction}') and (
                    file_name.endswith('.png')
                ):
                    image_path = os.path.join(path, file_name)
                    # image = Image.open(image_path)
                    self.textures[direction].append(arcade.load_texture(image_path))

            self._number_of_textures[direction] = len(self.textures[direction])

    def get_next_texture(self, direction: str) -> Tuple[arcade.Texture, bool]:
        """Get next texture."""
        current_texture = self.textures[direction][self.counters[direction]]
        self.counters[direction] += 1
        if self.counters[direction] >= self._number_of_textures[direction]:
            # Animation reached its final texture, reset the counter to the first image
            self._reset_index(direction)
            return current_texture, True
        else:
            # Animation has not reached its final texture yet
            return current_texture, False

    def _reset_index(self, direction: str):
        self.counters[direction] = 0
