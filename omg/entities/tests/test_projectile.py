import unittest
from unittest.mock import MagicMock
import math
import os
from omg.entities.projectile import Projectile, ProjectileShotEvent, FireballFactory, IceShardFactory
from omg.entities.tests import TEST_IMAGE_FILE

class TestProjectile(unittest.TestCase):

    def test_initialization(self):
        """Test initialization of the Projectile class."""
        projectile = Projectile(
            name="Fireball",
            image_file=TEST_IMAGE_FILE,
            scale=0.05,
            damage=25,
            speed=5,
            init_px=100,
            init_py=100,
            angle=45
        )
        self.assertEqual(projectile.name, "Fireball")
        self.assertEqual(projectile.damage, 25)
        self.assertEqual(projectile.speed, 5)
        self.assertEqual(projectile.center_x, 100)
        self.assertEqual(projectile.center_y, 100)
        self.assertEqual(projectile.angle, 45)

        expected_change_x = 5 * math.cos(math.radians(45 + 90))
        expected_change_y = 5 * math.sin(math.radians(45 + 90))
        self.assertAlmostEqual(projectile.change_x, expected_change_x)
        self.assertAlmostEqual(projectile.change_y, expected_change_y)

class TestProjectileShotEvent(unittest.TestCase):

    def test_event(self):
        """Test the ProjectileShotEvent class."""
        mock_projectile = MagicMock()
        mock_projectile.event_type = "projectile_shot"
        event = ProjectileShotEvent(mock_projectile)
        self.assertEqual(event.projectile.event_type, "projectile_shot")
        self.assertEqual(event.projectile, mock_projectile)

class TestFireballFactory(unittest.TestCase):

    def test_create(self):
        """Test FireballFactory creation of Projectiles."""
        factory = FireballFactory()
        projectile = factory.create(init_px=150, init_py=200, angle=30)

        self.assertEqual(projectile.name, "FireballFactory")
        self.assertEqual(projectile.scale, 0.05)
        self.assertEqual(projectile.damage, 25)
        self.assertEqual(projectile.speed, 5)
        self.assertEqual(projectile.center_x, 150)
        self.assertEqual(projectile.center_y, 200)
        self.assertEqual(projectile.angle, 30)

        expected_change_x = 5 * math.cos(math.radians(30 + 90))
        expected_change_y = 5 * math.sin(math.radians(30 + 90))
        self.assertAlmostEqual(projectile.change_x, expected_change_x)
        self.assertAlmostEqual(projectile.change_y, expected_change_y)

class TestIceShardFactory(unittest.TestCase):

    def test_create(self):
        """Test IceShardFactory creation of Projectiles."""
        factory = IceShardFactory()
        projectile = factory.create(init_px=200, init_py=250, angle=60)

        self.assertEqual(projectile.name, "IceShardFactory")
        self.assertEqual(projectile.scale, 0.05)
        self.assertEqual(projectile.damage, 15)
        self.assertEqual(projectile.speed, 7)
        self.assertEqual(projectile.center_x, 200)
        self.assertEqual(projectile.center_y, 250)
        self.assertEqual(projectile.angle, 60)

        expected_change_x = 7 * math.cos(math.radians(60 + 90))
        expected_change_y = 7 * math.sin(math.radians(60 + 90))
        self.assertAlmostEqual(projectile.change_x, expected_change_x)
        self.assertAlmostEqual(projectile.change_y, expected_change_y)

if __name__ == "__main__":
    unittest.main()
