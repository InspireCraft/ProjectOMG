from PIL import Image
import os

# Load the spritesheet image
spritesheet = Image.open("C:/Users/Admin/Desktop/2D_Sprite_Animations/demo_2/sprites_universal.png")

# Define the size of each sprite (assuming uniform size)
sprite_width = 64
sprite_height = 64

# Define the rows and columns in the spritesheet
rows = 46  # Number of rows in the spritesheet
cols = 13  # Number of columns in the spritesheet

# Define the animations and their respective frames
animations = {
    "Cast_Up": list(range(13*0, 13*0+7)),
    "Cast_Left": list(range(13*1, 13*1+7)),
    "Cast_Down": list(range(13*2, 13*2+7)),
    "Cast_Right": list(range(13*3, 13*3+7)),

    "Thrust_Up": list(range(13*4, 13*4+8)),
    "Thrust_Left": list(range(13*5, 13*5+8)),
    "Thrust_Down": list(range(13*6, 13*6+8)),
    "Thrust_Right": list(range(13*7, 13*7+8)),

    "Walk_Up": list(range(13*8, 13*8+9)),
    "Walk_Left": list(range(13*9, 13*9+9)),
    "Walk_Down": list(range(13*10, 13*10+9)),
    "Walk_Right": list(range(13*11, 13*11+9)),

    "Slash_Up": list(range(13*12, 13*12+6)),
    "Slash_Left": list(range(13*13, 13*13+6)),
    "Slash_Down": list(range(13*14, 13*14+6)),
    "Slash_Right": list(range(13*15, 13*15+6)),

    "BackSlash_Up": reversed(list(range(13*12, 13*12+6))),
    "BackSlash_Left": reversed(list(range(13*13, 13*13+6))),
    "BackSlash_Down": reversed(list(range(13*14, 13*14+6))),
    "BackSlash_Right": reversed(list(range(13*15, 13*15+6))),

    "Shoot_Up": list(range(13*16, 13*16+12)),
    "Shoot_Left": list(range(13*17, 13*17+12)),
    "Shoot_Down": list(range(13*18, 13*18+12)),
    "Shoot_Right": list(range(13*19, 13*19+12)),

    "Die": list(range(13*20, 13*20+6)),

    # "Climb": list(range(13*21, 13*21+6)),

    # "Idle_Up": list(range(13*22, 13*22+2)),
    # "Idle_Left": list(range(13*23, 13*23+2)),
    # "Idle_Down": list(range(13*24, 13*24+2)),
    # "Idle_Right": list(range(13*25, 13*25+2)),

    # "Combat_Up": list(range(13*22+2, 13*22+4)),
    # "Combat_Left": list(range(13*23+2, 13*23+4)),
    # "Combat_Down": list(range(13*24+2, 13*24+4)),
    # "Combat_Right": list(range(13*25+2, 13*25+4)),

    # "Jump_Up": list(range(13*26, 13*22+5)),
    # "Jump_Left": list(range(13*27, 13*23+5)),
    # "Jump_Down": list(range(13*28, 13*24+5)),
    # "Jump_Right": list(range(13*29, 13*25+5)),

    # "Run_Up": list(range(13*34, 13*34+8)),
    # "Run_Left": list(range(13*35, 13*35+8)),
    # "Run_Down": list(range(13*36, 13*36+8)),
    # "Run_Right": list(range(13*37, 13*37+8)),

    # # Add more animations and their frame ranges as needed
}

# Directory to save the cut sprites
dummy = "demo_2"
output_dir = f"C:/Users/Admin/Desktop/2D_Sprite_Animations/{dummy}/sprites"
os.makedirs(output_dir, exist_ok=True)

# Loop through the animations and frames to cut and save each sprite
for animation, frames in animations.items():
    for i, frame in enumerate(frames):
        # Calculate the position of the sprite in the spritesheet
        x = (frame % cols) * sprite_width
        y = (frame // cols) * sprite_height

        # Crop the sprite
        sprite = spritesheet.crop((x, y, x + sprite_width, y + sprite_height))

        # Save the sprite with the appropriate name
        sprite_name = f"{animation}{i}.png"
        sprite.save(os.path.join(output_dir, sprite_name))

print("Sprites have been cut and saved successfully.")
