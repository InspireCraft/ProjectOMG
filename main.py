import arcade
import logging
from omg.core.game_window import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, GameWindow


def main():
    """Start the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
