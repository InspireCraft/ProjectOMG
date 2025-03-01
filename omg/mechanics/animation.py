import os
from typing import Tuple

import arcade


class Animation():
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
                if file_name.startswith(f'{action}_{direction}') and file_name.endswith('.png'):
                    image_path = os.path.join(path, file_name)
                    # image = Image.open(image_path)
                    self.textures[direction].append(arcade.load_texture(image_path))

            self._number_of_textures[direction] = len(self.textures[direction])

    def get_next_texture(self, direction: str) -> Tuple[arcade.Texture, bool]:
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



if __name__ == '__main__':
    path = 'omg/mechanics/backslash'
    path = 'omg/assets/images/characters/demo_archer_2/sprites/'
    our_animations = ["idle", "walk", "slash", "spellcast", "thrust", "shoot", "die", "backslash"]
    animation = Animation(path, 'backslash')

    all_animations = {}
    for action in our_animations:
        all_animations[action] = Animation('omg/assets/images/characters/demo_archer_2/sprites/', action)


    for action in all_animations.keys():
        animation:Animation = all_animations[action]
        for direction in animation.textures.keys():
            print(action, direction, animation._number_of_textures[direction])

    print(all_animations)
    print(animation._number_of_textures)
