import arcade
import logging
from omg.core.game_window import GameView, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


def main():
    """Start the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView(window=window)
    window.show_view(start_view)
    start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()
