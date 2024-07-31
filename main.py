import arcade
import logging
from omg.core.game_window import GameWindow


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    window = GameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
