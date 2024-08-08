import logging
import unittest
from unittest.mock import MagicMock, patch
from omg.structural.observer import Event, Observer, ObservableSprite


class TestEvent(unittest.TestCase):

    def test_event_initialization(self):
        event = Event("test_event")
        self.assertEqual(event.event_type, "test_event")


class TestObserver(unittest.TestCase):

    def test_observer_registration_and_event_handling(self):
        observer = Observer()
        mock_handler = MagicMock()
        observer.register_handler("test_event", mock_handler)

        # Create a mock event
        event = Event("test_event")

        # Handle the event
        observer.on_event(event)

        # Check if the handler was called
        mock_handler.assert_called_once_with(event)

    def test_observer_without_handler(self):
        observer = Observer()
        event = Event("unhandled_event")

        # Capture the output using a mock for print
        with self.assertLogs(level="WARNING") as log:
            observer.on_event(event)

        # Verify that "No handler for event type" message is in the logs
        self.assertIn(
            "WARNING:root:No handler for event type:unhandled_event", log.output[0]
        )


class TestObservableSprite(unittest.TestCase):

    def test_observable_sprite_observer_management(self):
        sprite = ObservableSprite()
        observer = Observer()

        # Add observer
        sprite.add_observer(observer)
        self.assertIn(observer, sprite.observers)

        # Remove observer
        sprite.remove_observer(observer)
        self.assertNotIn(observer, sprite.observers)


if __name__ == "__main__":
    unittest.main()
