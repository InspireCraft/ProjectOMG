import os
import json
from typing import Dict

ELEMENTS_JSON_DIR = os.path.join(os.path.dirname(__file__), "Elements.JSON")


class DotDict(dict):
    """Convert dictionary to a format to call attributes with dot notation."""

    def __getattr__(self, key):
        """Get dictionary item as attribute.Convert nested dictionaries to DotDict."""
        value = self.get(key, None)
        if isinstance(value, dict):
            value = DotDict(value)
        return value

    def __setattr__(self, attr, value):
        """Set a dictionary item using attribute assignment syntax."""
        self[attr] = value


with open(ELEMENTS_JSON_DIR, "r") as file:
    ELEMENTS: Dict[str, Dict] = json.load(file)

# Convert nested dictionaries to DotDict instances
ELEMENTS: DotDict[str, DotDict] = DotDict(ELEMENTS)

