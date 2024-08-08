import unittest
from unittest.mock import patch, call
import arcade

from omg.entities.obstacle import Obstacle
from omg.entities.tests import TEST_IMAGE_FILE

class TestObstacle(unittest.TestCase):

    def setUp(self):
        self.image_file = TEST_IMAGE_FILE
        self.scale = 1.0
        self.health = 100
        self.obstacle = Obstacle(self.image_file, self.scale, self.health)

    def test_initial_health(self):
        self.assertEqual(self.obstacle.max_health, self.health)
        self.assertEqual(self.obstacle.current_health, self.health)

    def test_take_damage(self):
        damage = 30
        self.obstacle.take_damage(damage)
        self.assertEqual(self.obstacle.current_health, self.health - damage)

    def test_take_damage_kill(self):
        damage = 100
        with patch.object(self.obstacle, 'kill') as mock_kill:
            self.obstacle.take_damage(damage)
            self.assertEqual(self.obstacle.current_health, 0)
            mock_kill.assert_called_once()

    def test_draw(self):
        with patch('arcade.Sprite.draw') as mock_draw, \
             patch.object(self.obstacle, '_draw_health_bar') as mock_draw_health_bar:
            self.obstacle.draw()
            mock_draw.assert_called_once()
            mock_draw_health_bar.assert_called_once()

    def test_draw_health_bar(self):
        with patch('arcade.draw_rectangle_filled') as mock_draw_rectangle_filled:
            self.obstacle._draw_health_bar()
            health_bar_width = 50
            health_bar_height = 5
            health_bar_x = self.obstacle.center_x
            health_bar_y = self.obstacle.center_y + self.obstacle.height / 2 + 10
            calls = [
                call(
                    health_bar_x,
                    health_bar_y,
                    health_bar_width,
                    health_bar_height,
                    arcade.color.RED,
                ),
                call(
                    health_bar_x,
                    health_bar_y,
                    health_bar_width * (self.obstacle.current_health / self.obstacle.max_health),
                    health_bar_height,
                    arcade.color.GREEN,
                )
            ]
            mock_draw_rectangle_filled.assert_has_calls(calls, any_order=True)

    def test_draw_health_bar_after_damage(self):
        damage = 30
        self.obstacle.take_damage(damage)
        with patch('arcade.draw_rectangle_filled') as mock_draw_rectangle_filled:
            self.obstacle._draw_health_bar()
            health_bar_width = 50
            health_bar_height = 5
            health_bar_x = self.obstacle.center_x
            health_bar_y = self.obstacle.center_y + self.obstacle.height / 2 + 10
            current_health_width = health_bar_width * (
                self.obstacle.current_health / self.obstacle.max_health
            )
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

if __name__ == "__main__":
    unittest.main()
