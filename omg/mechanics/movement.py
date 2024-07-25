import math

class PlayerMovement:
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

    # TODO: on_key_press and on_key_release can be simplified to single method,
    # TODO: make calculate_displacement_directions static
    def on_key_press(self, key, modifiers):
        if key == self.key_forward:
            self.pressed_forward = True
        elif key == self.key_backward:
            self.pressed_backward = True
        elif key == self.key_left:
            self.pressed_left = True
        elif key == self.key_right:
            self.pressed_right = True

        [self.change_direction_x, self.change_direction_y] = self.calculate_displacement_directions()


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == self.key_forward:
            self.pressed_forward = False
        elif key == self.key_backward:
            self.pressed_backward = False
        elif key == self.key_left:
            self.pressed_left = False
        elif key == self.key_right:
            self.pressed_right = False

        [self.change_direction_x, self.change_direction_y] = self.calculate_displacement_directions()


    def calculate_displacement_directions(self):
        forward = 1 if self.pressed_forward else 0
        backward = -1 if self.pressed_backward else 0
        left = -1 if self.pressed_left else 0
        right = 1 if self.pressed_right else 0

        change_direction_x = left + right
        change_direction_y = forward + backward

        return change_direction_x, change_direction_y

    @staticmethod
    def face_mouse(mouse_x, mouse_y, center_x, center_y):
        # angle = 0 on +y axis(TOP), increases counter-clockwise
        return math.atan2(mouse_y - center_y, mouse_x - center_x) - math.pi/2


class MouseDirected(PlayerMovement):
    def calculate_player_state(self, center_x, center_y, mouse_x, mouse_y, mov_speed_lr, mov_speed_ud, *args, **_ignored):

        # Velocity is defined relative to where the player looks.
        # Map it to the coordinate system of the Window by rotation
        angle_rad = self.face_mouse(mouse_x, mouse_y, center_x, center_y)
        angle = math.degrees(angle_rad)
        cos_ang = math.cos(angle_rad)
        sin_ang = math.sin(angle_rad)
        # mov_speed_lr -> vx_player , mov_speed_ud -> vy_player
        vx_player = mov_speed_lr * self.change_direction_x
        vy_player = mov_speed_ud * self.change_direction_y
        vx_wrt_ground = cos_ang * vx_player - sin_ang * vy_player
        vy_wrt_ground = sin_ang * vx_player + cos_ang * vy_player

        center_x += vx_wrt_ground
        center_y += vy_wrt_ground

        # TODO: return PlayerState or PlayerPose object
        return center_x, center_y, angle
class CompassDirected(PlayerMovement):
    def calculate_player_state(self, center_x, center_y, mouse_x, mouse_y, mov_speed_lr, mov_speed_ud, *args, **_ignored):
        center_x += mov_speed_lr * self.change_direction_x
        center_y += mov_speed_ud * self.change_direction_y
        angle_rad = self.face_mouse(mouse_x, mouse_y, center_x, center_y)
        angle = math.degrees(angle_rad)
        # TODO: return PlayerState or PlayerPose object
        return center_x, center_y, angle
