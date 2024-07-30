from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def on_event(self, event_type: str, *args, **kwargs):
        """Handle the event notification with event type and data."""
        pass
