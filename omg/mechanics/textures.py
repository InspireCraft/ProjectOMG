import arcade           

class Textures():
    
    def __init__(self, sprite_path):

        self.animation_types = ["idle", "walk", "slash", "spellcast", "thrust", "shoot", "die"]
        self.direction_types = ["up", "down", "left", "right"]
        self.idle_length = 1
        self.walk_length = 9
        self.slash_length = 6
        self.spellcast_length = 7
        self.thrust_length = 8
        self.shoot_length = 12
        self.die_length = 6

        for animation in self.animation_types:
            for direction in self.direction_types:
                setattr(self, f"{animation}_{direction}", 
                        [arcade.load_texture(f"{sprite_path}/{animation}_{direction}{i}.png") for i in range(getattr(self, f"{animation}_length"))])
            setattr(self, animation, getattr(self, f"{animation}_down"))
 
        # Load textures for different animations
        # self.idle = []
        # self.walk = []
        # self.slash = []
        # self.spellcast = []
        # self.thrust = []
        # self.shoot = []
        # self.die = []

        # self.idle = [arcade.load_texture(f"{sprite_path}/Walk_Down{i}.png") for i in range(1)]
        # self.walk = [arcade.load_texture(f"{sprite_path}/Walk_Down{i}.png") for i in range(9)]
        # self.slash = [arcade.load_texture(f"{sprite_path}/Slash_Down{i}.png") for i in range(6)]
        # self.spellcast = [arcade.load_texture(f"{sprite_path}/Cast_Down{i}.png") for i in range(7)]
        # self.thrust = [arcade.load_texture(f"{sprite_path}/Thrust_Down{i}.png") for i in range(8)]
        # self.shoot = [arcade.load_texture(f"{sprite_path}/Shoot_Down{i}.png") for i in range(12)]
        # self.die = [arcade.load_texture(f"{sprite_path}/Die{i}.png") for i in range(6)]

        # self.idle_up = [arcade.load_texture(f"{sprite_path}/Walk_Up{i}.png") for i in range(1)]
        # self.idle_down = [arcade.load_texture(f"{sprite_path}/Walk_Down{i}.png") for i in range(1)]
        # self.idle_left = [arcade.load_texture(f"{sprite_path}/Walk_Left{i}.png") for i in range(1)]
        # self.idle_right = [arcade.load_texture(f"{sprite_path}/Walk_Right{i}.png") for i in range(1)]
        # self.walk_up = [arcade.load_texture(f"{sprite_path}/Walk_Up{i}.png") for i in range(9)]
        # self.walk_down = [arcade.load_texture(f"{sprite_path}/Walk_Down{i}.png") for i in range(9)]
        # self.walk_left = [arcade.load_texture(f"{sprite_path}/Walk_Left{i}.png") for i in range(9)]
        # self.walk_right = [arcade.load_texture(f"{sprite_path}/Walk_Right{i}.png") for i in range(9)]
        # self.slash_up = [arcade.load_texture(f"{sprite_path}/Slash_Up{i}.png") for i in range(6)]
        # self.slash_down = [arcade.load_texture(f"{sprite_path}/Slash_Down{i}.png") for i in range(6)]
        # self.slash_left = [arcade.load_texture(f"{sprite_path}/Slash_Left{i}.png") for i in range(6)]
        # self.slash_right = [arcade.load_texture(f"{sprite_path}/Slash_Right{i}.png") for i in range(6)]
        # self.spellcast_up = [arcade.load_texture(f"{sprite_path}/Cast_Up{i}.png") for i in range(7)]
        # self.spellcast_down = [arcade.load_texture(f"{sprite_path}/Cast_Down{i}.png") for i in range(7)]
        # self.spellcast_left = [arcade.load_texture(f"{sprite_path}/Cast_Left{i}.png") for i in range(7)]
        # self.spellcast_right = [arcade.load_texture(f"{sprite_path}/Cast_Right{i}.png") for i in range(7)]
        # self.thrust_up = [arcade.load_texture(f"{sprite_path}/Thrust_Up{i}.png") for i in range(8)]
        # self.thrust_down = [arcade.load_texture(f"{sprite_path}/Thrust_Down{i}.png") for i in range(8)]
        # self.thrust_left = [arcade.load_texture(f"{sprite_path}/Thrust_Left{i}.png") for i in range(8)]
        # self.thrust_right = [arcade.load_texture(f"{sprite_path}/Thrust_Right{i}.png") for i in range(8)]
        # self.shoot_up = [arcade.load_texture(f"{sprite_path}/Shoot_Up{i}.png") for i in range(12)]
        # self.shoot_down = [arcade.load_texture(f"{sprite_path}/Shoot_Down{i}.png") for i in range(12)]
        # self.shoot_left = [arcade.load_texture(f"{sprite_path}/Shoot_Left{i}.png") for i in range(12)]
        # self.shoot_right = [arcade.load_texture(f"{sprite_path}/Shoot_Right{i}.png") for i in range(12)]
        # self.die_up = [arcade.load_texture(f"{sprite_path}/Die{i}.png") for i in range(6)]
        # self.die_down = [arcade.load_texture(f"{sprite_path}/Die{i}.png") for i in range(6)]
        # self.die_left = [arcade.load_texture(f"{sprite_path}/Die{i}.png") for i in range(6)]
        # self.die_right = [arcade.load_texture(f"{sprite_path}/Die{i}.png") for i in range(6)]

        # Animation indices and timers
        self.idle_index = 0
        self.walk_index = 0
        self.slash_index = 0
        self.spellcast_index = 0
        self.thrust_index = 0
        self.shoot_index = 0
        self.die_index = 0

    def increment_index(self, state):
        if state == "idle":
            self.idle_index = (self.idle_index + 1) % self.idle_length
        if state == "walk":
            self.walk_index = (self.walk_index + 1) % self.walk_length
        if state == "slash":
            self.slash_index += 1
        if state == "spellcast":
            self.spellcast_index += 1
        if state == "thrust":
            self.thrust_index += 1
        if state == "shoot":
            self.shoot_index += 1
        if state == "die":
            self.die_index += 1 

    def reset_index(self, state):
        setattr(self, f"{state}_index", 0)
        # if state == "idle":
        #     self.idle_index = 0
        # if state == "walk":
        #     self.walk_index = 0
        # if state == "slash":
        #     self.slash_index = 0
        # if state == "spellcast":
        #     self.spellcast_index = 0
        # if state == "thrust":
        #     self.thrust_index = 0
        # if state == "shoot":
        #     self.shoot_index = 0
        # if state == "die":
        #     self.die_index = 0

    def set_texture(self, direction):
        for animation in self.animation_types:
            setattr(self, animation, getattr(self, f"{animation}_{direction}"))
        # self.idle = getattr(self, f"idle_{direction}")
        # self.walk = getattr(self, f"walk_{direction}")
        # self.slash = getattr(self, f"slash_{direction}")
        # self.spellcast = getattr(self, f"spellcast_{direction}")
        # self.thrust = getattr(self, f"thrust_{direction}")
        # self.shoot = getattr(self, f"shoot_{direction}")
        # self.die = self.die



