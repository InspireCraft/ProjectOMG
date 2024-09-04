import os
import json
from typing import Dict

ELEMENTS_JSON_DIR = os.path.join(os.path.dirname(__file__), "Elements.JSON")


class DotDict(dict):
    """Convert dictionary to a format to call attributes with dot notation."""

    def __getattr__(self, attr):
        """Get dictionary item as attribute.Convert nested dictionaries to DotDict."""
        value = self.get(attr)
        if isinstance(value, dict):
            value = DotDict(value)
        return value

    def __setattr__(self, attr, value):
        """Set a dictionary item using attribute assignment syntax."""
        self[attr] = value


# Recursively convert the dictionary and all its nested dictionaries to DotDict
def to_dotdict(d) -> DotDict:
    """Convert dictionary and its nested ones to DotDict."""
    if isinstance(d, dict):
        return DotDict({k: to_dotdict(v) for k, v in d.items()})
    return d


with open(ELEMENTS_JSON_DIR, "r") as file:
    ELEMENTS: Dict[str, Dict] = json.load(file)

# Convert nested dictionaries to DotDict instances
ELEMENTS: DotDict[str, DotDict] = to_dotdict(ELEMENTS)
