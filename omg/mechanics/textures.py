from omg.mechanics.animation import Animation


class Textures():

    def __init__(self, sprite_path):

        self.animation_types = ["idle", "walk", "slash", "spellcast", "thrust", "shoot", "die"]
        self.all_animations = {}
        for action in self.animation_types:
            self.all_animations[action] = Animation(sprite_path, action)

        self.active_direction = "down"

    def increment_index(self, state)->bool:

        current_animation: Animation = self.all_animations[state]
        return current_animation.increment_index(self.active_direction)


    def reset_index(self, state):
        current_animation: Animation = self.all_animations[state]
        current_animation.reset_index(self.active_direction)

    def set_direction(self, direction):
        self.active_direction = direction


