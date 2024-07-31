from typing import List

import arcade


class Event:
    """Base class for events in the Observer pattern."""

    def __init__(self, event_type: str):
        """
        Parameters
        ----------
        event_type : str
            The type of the event.
        """
        self.event_type = event_type


class Observer:
    """Observer for game-related events, managing event handling.

    Attributes
    ----------
    game_window : GameWindow
        The game window instance that this observer interacts with.
    _handlers : dict
        A dictionary mapping event types to handler methods.
    """

    def __init__(self):
        self._handlers: dict = {}

    def register_handler(self, event_type: str, handler):
        """Register a new event handler for a specific event type.

        Parameters
        ----------
        event_type : str
            The type of event the handler will process.
        handler : function
            The handler function to be called when the event occurs.
        """
        self._handlers[event_type] = handler

    def on_event(self, event: Event):
        """Handle an event by dispatching to the appropriate handler.

        Parameters
        ----------
        event : Event
            The event to handle.
        """
        handler = self._handlers.get(event.event_type)
        if handler:
            handler(event)
        else:
            # TODO: Change to a logging call
            print(f"No handler for event type: {event.event_type}")


class ObservableSprite(arcade.Sprite):
    observers: List[Observer] = []

    def add_observer(self, observer: Observer):
        """Add an observer to the list."""
        self.observers.append(observer)

    def remove_observer(self, observer: Observer):
        """Remove an observer from the list."""
        self.observers.remove(observer)

    def notify_observers(self, event: Event):
        """Notify all observers of an event."""
        for observer in self.observers:
            observer.on_event(event)
