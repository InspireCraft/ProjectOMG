import unittest
from unittest.mock import MagicMock, patch
import arcade
import logging
from omg.entities.player import Player
from omg.entities.obstacle import Obstacle
from omg.entities.projectile import FireballFactory, IceShardFactory, ProjectileShotEvent
from omg.mechanics.physics import PhysicsEngineBoundary
from omg.structural.observer import Observer
from omg.core.game_window import GameWindow  # Adjust import according to your project structure

class TestGameWindow(unittest.TestCase):

    @patch.object(arcade.Window, '__init__', MagicMock())
    @patch('arcade.load_texture')
    def test_setup(self, mock_load_texture):
        """Test the setup of the game window."""
        mock_load_texture.return_value = MagicMock()

        window = GameWindow()
        window.setup()

        self.assertIsInstance(window.observer, Observer)
        self.assertIsInstance(window.player, Player)
        self.assertIsInstance(window.obstacles, arcade.SpriteList)
        self.assertIsInstance(window.projectiles, arcade.SpriteList)
        self.assertIsInstance(window.physics_engine, PhysicsEngineBoundary)
        self.assertGreater(len(window.skill_icons), 0)  # Ensure that skill icons are loaded

        # Check that projectiles were added
        self.assertEqual(len(window.player.projectile_types), 2)
        self.assertIn(FireballFactory, window.player.projectile_types)
        self.assertIn(IceShardFactory, window.player.projectile_types)

    @patch.object(arcade.Window, '__init__', MagicMock())
    def test_update(self):
        """Test the update method."""
        window = GameWindow()
        window.setup()

        # Mock the update methods
        window.player.update = MagicMock()
        window.obstacles.update = MagicMock()
        window.physics_engine.update = MagicMock()
        window.projectiles.update = MagicMock()

        # Call update
        window.update(1.0)

        # Verify updates were called
        window.player.update.assert_called_once_with(window.mouse_x, window.mouse_y, 1.0)
        window.obstacles.update.assert_called_once()
        window.physics_engine.update.assert_called_once()
        window.projectiles.update.assert_called_once()

    @patch.object(arcade.Window, '__init__', MagicMock())
    def test_on_projectile_shot(self):
        """Test the _on_projectile_shot method."""
        window = GameWindow()
        window.setup()

        # Create a mock projectile
        projectile = MagicMock()
        event = ProjectileShotEvent(projectile)

        # Call the method
        window._on_projectile_shot(event)

        # Verify the projectile was added
        self.assertIn(projectile, window.projectiles)

    @patch.object(arcade.Window, '__init__', MagicMock())
    @patch('arcade.start_render')
    def test_on_draw(self, mock_start_render):
        """Test the on_draw method."""
        # Initialize and setup GameWindow
        window = GameWindow()
        window.setup()

        # Set mock return values
        window.player = MagicMock()
        window.obstacles = MagicMock()
        window.projectiles = MagicMock()
        window._draw_ui = MagicMock()

        # Call on_draw
        window.on_draw()

        # Verify mock calls
        mock_start_render.assert_called_once()
        window._draw_ui.assert_called_once()

    @patch.object(logging, '__init__', MagicMock())
    @patch.object(arcade.Window, '__init__', MagicMock())
    @patch('arcade.draw_texture_rectangle')
    @patch('arcade.draw_rectangle_outline')
    def test_ui_draw(self, mock_draw_rectangle_outline, mock_draw_texture_rectangle):
        """Test UI drawing logic."""
        mock_draw_texture_rectangle.return_value = None
        mock_draw_rectangle_outline.return_value = None

        window = GameWindow()
        window.setup()

        # # Call the _draw_ui method
        window._draw_ui()

        # # Check that the skill icons are drawn
        self.assertGreater(mock_draw_texture_rectangle.call_count, 0)
        self.assertGreater(mock_draw_rectangle_outline.call_count, 0)

if __name__ == "__main__":
    unittest.main()
