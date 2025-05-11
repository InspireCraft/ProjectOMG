from typing import Dict


import arcade
import arcade.key

from omg.core.views import (
    GameView,
    PauseView,
    SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
)


class GameWindow(arcade.Window):
    """Main game window."""

    GAME_VIEW_KEY = "game"
    PAUSE_VIEW_KEY = "pause"

    def __init__(self, width: int, height: int, title: str):
        super().__init__(width, height, title)
        self._views: Dict[str, arcade.View] = None

    def setup(self):
        """Setup the game."""
        self._views: Dict[str, arcade.View] = {}
        self._views[self.GAME_VIEW_KEY] = GameView(window=self)
        self._views[self.PAUSE_VIEW_KEY] = PauseView(window=self)
        self._view_state = True  # Binary state to track the active state

        self._game_view.setup()
        self.show_view(self._game_view)

    @property
    def _game_view(self) -> GameView:
        """Define self._game_view which always refers to a View in self._views."""
        return self._views.get(self.GAME_VIEW_KEY, None)

    @property
    def _pause_view(self) -> PauseView:
        """Define self._pause_view which always refers to a View in self._views."""
        return self._views.get(self.PAUSE_VIEW_KEY, None)

    def on_key_press(self, key, modifiers):
        """Key press logic."""
        if key == arcade.key.ESCAPE:
            # NOTE: This logic needs a refactor when the number of views exceeds
            # 2.
            self._view_state = not self._view_state
            if self._view_state:
                self.show_view(self._game_view)
            else:
                self._pause_view.update_view_to_draw(self._game_view)
                self.show_view(self._pause_view)


def main():
    """Main application code."""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()
