import os
import json
from typing import Dict

ELEMENTS_JSON_DIR = os.path.join(os.path.dirname(__file__), "Elements.JSON")

with open(ELEMENTS_JSON_DIR, "r") as file:
    ELEMENTS: Dict[str, Dict] = json.load(file)
