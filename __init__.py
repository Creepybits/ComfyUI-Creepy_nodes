"""Top-level package for Creepy_nodes."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

__author__ = "Creepybits"
__email__ = "work@zanno.se"
__version__ = "0.0.1"

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

WEB_DIRECTORY = "./web" # Or the correct path to your web directory
