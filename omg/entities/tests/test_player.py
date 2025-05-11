import unittest
from unittest.mock import patch, MagicMock, call
from venv import create
import arcade
from omg.entities.player import CircularBuffer, Player
from omg.entities.tests import TEST_IMAGE_FILE

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player(
            name="TestPlayer",
            char_class="Warrior",
            image_file=TEST_IMAGE_FILE,
            scale=1.0
        )

    def test_on_key_press(self):
        with patch.object(self.player.movement_logic, 'on_key_press') as mock_on_key_press:
            self.player.on_key_press(arcade.key.W, None)
            mock_on_key_press.assert_called_once_with(arcade.key.W, None)

        with patch.object(self.player, 'shoot') as mock_shoot:
            self.player.on_key_press(arcade.key.H, None)
            mock_shoot.assert_called_once()

    def test_on_key_release(self):
        with patch.object(self.player.movement_logic, 'on_key_release') as mock_on_key_release:
            self.player.on_key_release(arcade.key.W, None)
            mock_on_key_release.assert_called_once_with(arcade.key.W, None)

    def test_update(self):
        with patch.object(self.player.movement_logic, 'calculate_player_state', return_value=(1, 1, 45, 15)):
            with patch.object(self.player, '_regenerate_mana') as mock_regen_mana:
                self.player.update(mouse_x=200, mouse_y=200, delta_time=0.5)
                self.assertEqual(self.player.change_x, 1)
                self.assertEqual(self.player.change_y, 1)
                self.assertEqual(self.player.angle, 45)
                self.assertEqual(self.player.shoot_angle, 15)
                mock_regen_mana.assert_called_once_with(0.5)

    def test_shoot(self):
        with patch.object(self.player, 'notify_observers') as mock_notify_observers:

            mock_buffer = MagicMock()
            mock_skill = MagicMock(create=MagicMock())
            mock_skill_factory = MagicMock(return_value=mock_skill)
            mock_buffer.get_current = mock_skill_factory
            with patch.object(self.player, 'skills', mock_buffer):
                self.player.current_mana = 30
                self.player.shoot()
                self.assertLess(self.player.current_mana, 30)
                mock_notify_observers.assert_called_once()

    def test_shoot_no_mana(self):
        with patch.object(self.player, 'notify_observers') as mock_notify_observers:
            self.player.current_mana = 10
            self.player.shoot()
            mock_notify_observers.assert_not_called()

    def test_regen_mana(self):
        self.player.current_mana = 50
        self.player._regenerate_mana(delta_time=1.5)
        self.assertEqual(self.player.current_mana, 55)

    def test_draw(self):
        with patch('arcade.Sprite.draw') as mock_draw, \
             patch.object(self.player, '_draw_health_bar') as mock_draw_health_bar, \
             patch.object(self.player, '_draw_mana_bar') as mock_draw_mana_bar:
            self.player.draw()
            mock_draw.assert_called_once()
            mock_draw_health_bar.assert_called_once()
            mock_draw_mana_bar.assert_called_once()

    def test_draw_health_bar(self):
        with patch('arcade.draw_rectangle_filled') as mock_draw_rectangle_filled:
            self.player._draw_health_bar()
            health_bar_width = 50
            health_bar_height = 5
            health_bar_x = self.player.center_x
            health_bar_y = self.player.center_y + self.player.height / 2 + 10
            current_health_width = health_bar_width * (self.player.current_health / self.player.max_health)
            calls = [
                call(
                    health_bar_x,
                    health_bar_y,
                    health_bar_width,
                    health_bar_height,
                    arcade.color.RED,
                ),
                call(
                    health_bar_x - (health_bar_width - current_health_width) / 2,
                    health_bar_y,
                    current_health_width,
                    health_bar_height,
                    arcade.color.GREEN,
                )
            ]
            mock_draw_rectangle_filled.assert_has_calls(calls, any_order=True)

    def test_draw_mana_bar(self):
        with patch('arcade.draw_rectangle_filled') as mock_draw_rectangle_filled:
            self.player._draw_mana_bar()
            mana_bar_width = 50
            mana_bar_height = 5
            mana_bar_x = self.player.center_x
            mana_bar_y = self.player.center_y + self.player.height / 2 + 2
            current_mana_width = mana_bar_width * (self.player.current_mana / self.player.max_mana)
            calls = [
                call(
                    mana_bar_x,
                    mana_bar_y,
                    mana_bar_width,
                    mana_bar_height,
                    arcade.color.DARK_BLUE,
                ),
                call(
                    mana_bar_x - (mana_bar_width - current_mana_width) / 2,
                    mana_bar_y,
                    current_mana_width,
                    mana_bar_height,
                    arcade.color.LIGHT_BLUE,
                )
            ]
            mock_draw_rectangle_filled.assert_has_calls(calls, any_order=True)

if __name__ == "__main__":
    unittest.main()
