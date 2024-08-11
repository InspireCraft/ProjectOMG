from abc import ABC, abstractmethod
from typing import Generic, Iterator, List, TypeVar
import arcade

# Define a type variable T
T = TypeVar("T")


class Pickupable(arcade.Sprite, Generic[T]):
    """Class to represent objects which are pickupable from the environment.

    It holds an item which is to be delivered to an entity when it is picked up.
    """

    def __init__(
        self,
        image_file: str,
        scale: float,
        item: T,
        center_x: float,
        center_y: float,
        **kwargs
    ):
        super().__init__(
            image_file, scale=scale, center_x=center_x, center_y=center_y, **kwargs
        )
        self.item = item

    def get_item(self) -> T:
        """Return the item stored in the pickupable sprite."""
        return self.item


class ItemManager(ABC):
    """Abstract class to define the interfaces of each item manager should implement."""

    @abstractmethod
    def add_item(self, item: T):
        """Add an item to the manager."""
        pass


class CircularBuffer(ItemManager, Generic[T]):
    """
    Circular buffer to hold a determined size of items.

    Implements ItemManager interface

    """

    def __init__(self, max_size):
        self.buffer: List[T] = [None] * max_size  # Initialize with max size
        self.max_size = max_size
        self.current_size = 0
        self.index = 0

    def add_item(self, item: T):
        """
        Add item to the buffer. If the buffer is full, replace an item.

        Implements ItemManager add() interface
        """
        if self.current_size == self.max_size:
            self.index = (self.index + 1) % self.max_size
        else:
            self.index = self.current_size
        self.buffer[self.index] = item
        if self.current_size < self.max_size:
            self.current_size += 1

    def get_current(self) -> T:
        """Get the current item with respect to the current index."""
        if self.current_size == 0:
            return None
        return self.buffer[self.index]

    def get_current_index(self) -> int:
        """Return the current index."""
        return self.index

    def get_next(self) -> T:
        """Get next item with respect to the current index. Update the index."""
        if self.current_size == 0:
            return None
        self.index = (self.index + 1) % self.current_size
        return self.buffer[self.index]

    def get_prev(self) -> T:
        """Get previous item with respect to the current index. Update the index."""
        if self.current_size == 0:
            return None
        self.index = (self.index - 1) % self.current_size
        return self.buffer[self.index]

    def set_next(self):
        """Shift current index to the next item."""
        if self.current_size == 0:
            return
        self.index = (self.index + 1) % self.current_size

    def set_prev(self):
        """Shift current index to the previous item."""
        if self.current_size == 0:
            return
        self.index = (self.index - 1) % self.current_size

    def __iter__(self) -> Iterator[T]:
        """Iterate over the buffer from the start to the valid range."""
        start = 0
        end = self.current_size
        for i in range(start, end):
            yield self.buffer[i % self.max_size]
