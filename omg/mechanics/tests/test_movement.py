import unittest
import math
from omg.mechanics.movement import MouseDirected, CompassDirected

class TestPlayerMovement(unittest.TestCase):
    def setUp(self):
        self.forward = "w"
        self.backward = "s"
        self.left = "a"
        self.right = "d"
        self.mov_speed_lr = 5
        self.mov_speed_ud = 5
        self.center_x = 0
        self.center_y = 0
        self.mouse_x = 100
        self.mouse_y = 100

    def test_mouse_directed_movement(self):
        player = MouseDirected(self.forward, self.backward, self.left, self.right)

        # Simulate key presses
        player.on_key_press(self.forward, None)
        player.on_key_press(self.right, None)

        vx, vy, angle = player.calculate_player_state(
            self.center_x, self.center_y, self.mouse_x, self.mouse_y, self.mov_speed_lr, self.mov_speed_ud
        )

        expected_angle_rad = player.face_mouse(self.mouse_x, self.mouse_y, self.center_x, self.center_y)
        expected_angle = math.degrees(expected_angle_rad)
        cos_ang = math.cos(expected_angle_rad)
        sin_ang = math.sin(expected_angle_rad)

        expected_vx_player = self.mov_speed_lr * player.change_direction_x
        expected_vy_player = self.mov_speed_ud * player.change_direction_y
        expected_vx_wrt_ground = cos_ang * expected_vx_player - sin_ang * expected_vy_player
        expected_vy_wrt_ground = sin_ang * expected_vx_player + cos_ang * expected_vy_player

        self.assertAlmostEqual(vx, expected_vx_wrt_ground)
        self.assertAlmostEqual(vy, expected_vy_wrt_ground)
        self.assertAlmostEqual(angle, expected_angle)

    def test_compass_directed_movement(self):
        player = CompassDirected(self.forward, self.backward, self.left, self.right)

        # Simulate key presses
        player.on_key_press(self.forward, None)
        player.on_key_press(self.right, None)

        vx, vy, angle = player.calculate_player_state(
            self.center_x, self.center_y, self.mouse_x, self.mouse_y, self.mov_speed_lr, self.mov_speed_ud
        )

        expected_angle_rad = player.face_mouse(self.mouse_x, self.mouse_y, self.center_x, self.center_y)
        expected_angle = math.degrees(expected_angle_rad)

        expected_vx_wrt_ground = self.mov_speed_lr * player.change_direction_x
        expected_vy_wrt_ground = self.mov_speed_ud * player.change_direction_y

        self.assertAlmostEqual(vx, expected_vx_wrt_ground)
        self.assertAlmostEqual(vy, expected_vy_wrt_ground)
        self.assertAlmostEqual(angle, expected_angle)

    def test_on_key_press_release(self):
        player = MouseDirected(self.forward, self.backward, self.left, self.right)

        # Test key press
        player.on_key_press(self.forward, None)
        self.assertTrue(player.pressed_forward)
        self.assertEqual(player.change_direction_y, 1)

        player.on_key_press(self.backward, None)
        self.assertTrue(player.pressed_backward)
        self.assertEqual(player.change_direction_y, 0)

        player.on_key_press(self.left, None)
        self.assertTrue(player.pressed_left)
        self.assertEqual(player.change_direction_x, -1)

        player.on_key_press(self.right, None)
        self.assertTrue(player.pressed_right)
        self.assertEqual(player.change_direction_x, 0)

        # Test key release
        player.on_key_release(self.forward, None)
        self.assertFalse(player.pressed_forward)
        self.assertEqual(player.change_direction_y, -1)

        player.on_key_release(self.backward, None)
        self.assertFalse(player.pressed_backward)
        self.assertEqual(player.change_direction_y, 0)

        player.on_key_release(self.left, None)
        self.assertFalse(player.pressed_left)
        self.assertEqual(player.change_direction_x, 1)

        player.on_key_release(self.right, None)
        self.assertFalse(player.pressed_right)
        self.assertEqual(player.change_direction_x, 0)

if __name__ == "__main__":
    unittest.main()
