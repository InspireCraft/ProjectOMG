from abc import ABC, abstractmethod
import math
# import arcade
# import arcade.key


class PlayerMovement(ABC):
    """Player movement logic abstract base class."""

    def __init__(self, forward, backward, left, right):
        self.key_forward = forward
        self.key_backward = backward
        self.key_left = left
        self.key_right = right

        # These fields matter when moving the character
        self.change_direction_x = 0
        self.change_direction_y = 0

        # Track the current state of what key is pressed or released
        self.pressed_backward: bool = False
        self.pressed_forward: bool = False
        self.pressed_left: bool = False
        self.pressed_right: bool = False

        # Track animations
        self.move_direction = (0, 0)
        self.action_finished = 0

    @abstractmethod
    def calculate_player_state(
        self,
        center_x,
        center_y,
        mouse_x,
        mouse_y,
        mov_speed_lr,
        mov_speed_ud,
        *args,
        **_ignored
    ):
        """Given input player state, move the player."""
        pass

    # TODO: on_key_press and on_key_release can be simplified to single method,
    # TODO: make calculate_displacement_directions static
    def on_key_press(self, key, modifiers):
        """Called when the user presses a key."""
        if key == self.key_forward:
            self.pressed_forward = True
            self.move_direction = (self.move_direction[0], self.move_direction[1] + 1)
        elif key == self.key_backward:
            self.pressed_backward = True
            self.move_direction = (self.move_direction[0], self.move_direction[1] - 1)
        elif key == self.key_left:
            self.pressed_left = True
            self.move_direction = (self.move_direction[0] - 1, self.move_direction[1])
        elif key == self.key_right:
            self.pressed_right = True
            self.move_direction = (self.move_direction[0] + 1, self.move_direction[1])

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == self.key_forward:
            self.pressed_forward = False
            self.move_direction = (self.move_direction[0], self.move_direction[1] - 1)
        elif key == self.key_backward:
            self.pressed_backward = False
            self.move_direction = (self.move_direction[0], self.move_direction[1] + 1)
        elif key == self.key_left:
            self.pressed_left = False
            self.move_direction = (self.move_direction[0] + 1, self.move_direction[1])
        elif key == self.key_right:
            self.pressed_right = False
            self.move_direction = (self.move_direction[0] - 1, self.move_direction[1])

    def _calculate_displacement_directions(self):

        if self.action_finished:
            [change_direction_x, change_direction_y] = self.move_direction
        else:
            [change_direction_x, change_direction_y] = (0, 0)
        return change_direction_x, change_direction_y

    @staticmethod
    def face_mouse(mouse_x, mouse_y, center_x, center_y):
        """Calculates angle that would face the player to the mouse in radians."""
        # angle = 0 on +y axis(TOP), increases counter-clockwise
        return math.atan2(mouse_y - center_y, mouse_x - center_x) - math.pi / 2


class CompassDirected(PlayerMovement):
    """Movement logic that accepts the top of the window as the 'up' direction."""

    def calculate_player_state(
        self,
        center_x,
        center_y,
        mouse_x,
        mouse_y,
        mov_speed_lr,
        mov_speed_ud,
        *args,
        **_ignored
    ):
        """Given input player state, move the player.

        Velocity is defined relative to the Window.
        """
        [self.change_direction_x, self.change_direction_y] = (
            self._calculate_displacement_directions()
        )
        vx_wrt_ground = mov_speed_lr * self.change_direction_x
        vy_wrt_ground = mov_speed_ud * self.change_direction_y
        character_face_angle = 0  # Angle is always 0 to enable proper animations
        shoot_angle_rad = self.face_mouse(mouse_x, mouse_y, center_x, center_y)
        shoot_angle_deg = math.degrees(shoot_angle_rad)
        return vx_wrt_ground, vy_wrt_ground, character_face_angle, shoot_angle_deg
