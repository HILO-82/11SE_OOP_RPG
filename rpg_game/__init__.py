"""
RPG Game package initialization.

This module initializes the RPG game package and exports necessary classes.
"""

from .game import Game
from .character import Character
from .boss import Boss
from .sidekick import Sidekick
from .villain import Villain
from .inventory import Inventory, Item, Consumable, Armor
from .utils.logger import GameLogger
from .utils.console import clear_screen, press_enter, print_border

__all__ = [
    'Game',
    'Character',
    'Boss',
    'Sidekick',
    'Villain',
    'Inventory',
    'Item',
    'Consumable',
    'Armor',
    'GameLogger',
    'clear_screen',
    'press_enter',
    'print_border'
]
