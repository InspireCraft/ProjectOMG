from abc import ABC, abstractmethod
import arcade
import math
import os

ASSET_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "images")

class DotDict(dict):
    def __getattr__(self, attr):
        value = self.get(attr)
        if isinstance(value, dict):
            value = DotDict(value)
        return value

    def __setattr__(self, attr, value):
        self[attr] = value

# Recursively convert the dictionary and all its nested dictionaries to DotDict
def to_dotdict(d):
    if isinstance(d, dict):
        return DotDict({k: to_dotdict(v) for k, v in d.items()})
    return d

ELEMENTS = {
    "fire": {
        "image_file": os.path.join(ASSET_DIR, "skills", "elements", "fire.PNG"), 
        "scale": 0.05
    },
    "ice": {
        "img_file": os.path.join(ASSET_DIR, "skills", "elements", "ice.PNG"), 
        "scale": 0.05
    }
}

# Convert nested dictionaries to DotDict instances
elements = to_dotdict(elements)

    