import unittest
import arcade
from unittest.mock import MagicMock
from omg.mechanics.collision import handle_projectile_collisions

class TestHandleProjectileCollision(unittest.TestCase):

    def test_projectile_collision(self):
        """Test collision logic using MagicMocks.

        Using MagicMocks eliminate the need of creating actual objects.
        """
        projectile_1 = MagicMock()
        projectile_1.damage = 10
        projectile_2 = MagicMock()
        projectile_2.damage = 20
        projectiles = arcade.SpriteList()
        projectiles.append(projectile_1)
        projectiles.append(projectile_2)

        obstacles = arcade.SpriteList()
        obstacle1 = MagicMock()
        obstacle2 = MagicMock()
        obstacles.append(obstacle1)
        obstacles.append(obstacle2)

        # The side_effect attribute of a MagicMock can be used to define a
        # sequence of return values or behaviors for successive calls to the
        # mock function.
        arcade.check_for_collision_with_list = MagicMock(side_effect=[
            [obstacle1],  # projectile1 hits obstacle1
            []           # projectile2 hits no obstacles
        ])
        handle_projectile_collisions(projectiles, obstacles)
        obstacle1.take_damage.assert_called_once_with(10)
        obstacle2.take_damage.assert_not_called()
        projectile_1.kill.assert_called_once()
        projectile_2.kill.assert_not_called()

if __name__ == "__main__":
    unittest.main()
