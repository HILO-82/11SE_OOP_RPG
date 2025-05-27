"""
Inventory module for the RPG game.

This module manages items, equipment, and character inventories.
"""
import sys
import os
from typing import Dict, List, Optional, Type

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rpg_game.weapon import Weapon

class Item:
    """
    Base class for all game items.
    """
    def __init__(self, name: str, description: str, value: int = 0) -> None:
        """
        Initialize a new Item.
        
        Args:
            name: The item's name
            description: Description of the item
            value: The item's value (for trading)
        """
        self.name = name
        self.description = description
        self.value = value

class Consumable(Item):
    """
    Represents consumable items that can be used during combat.
    """
    def __init__(self, name: str, description: str, value: int, heal_amount: int) -> None:
        """
        Initialize a new Consumable.
        
        Args:
            name: The item's name
            description: Description of the item
            value: The item's value
            heal_amount: Amount of health restored when used
        """
        super().__init__(name, description, value)
        self.heal_amount = heal_amount

class Armor(Item):
    """
    Represents armor items that provide defense.
    """
    def __init__(self, name: str, description: str, value: int, defense_bonus: int) -> None:
        """
        Initialize a new Armor.
        
        Args:
            name: The item's name
            description: Description of the item
            value: The item's value
            defense_bonus: Amount of defense provided
        """
        super().__init__(name, description, value)
        self.defense_bonus = defense_bonus

class Inventory:
    """
    Manages a character's inventory of items and equipment.
    """
    def __init__(self) -> None:
        """
        Initialize a new Inventory.
        """
        self.items: Dict[str, dict] = {}  # item_name: {'item': Item, 'quantity': int}
        self.equipment: Dict[str, Item] = {
            'weapon': None,
            'armor': None
        }
        self.gold: int = 0

    def add_item(self, item: Item, quantity: int = 1) -> None:
        """
        Add an item to the inventory.
        
        Args:
            item: The item to add
            quantity: Number of items to add
        """
        if item.name in self.items:
            self.items[item.name]['quantity'] += quantity
        else:
            self.items[item.name] = {'item': item, 'quantity': quantity}

    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """
        Remove an item from the inventory.
        
        Args:
            item_name: Name of the item to remove
            quantity: Number of items to remove
            
        Returns:
            True if item was successfully removed, False otherwise
        """
        if item_name in self.items:
            if self.items[item_name]['quantity'] >= quantity:
                self.items[item_name]['quantity'] -= quantity
                if self.items[item_name]['quantity'] == 0:
                    del self.items[item_name]
                return True
        return False

    def equip_item(self, item: Item) -> bool:
        """
        Equip an item from the inventory.
        
        Args:
            item: The item to equip
            
        Returns:
            True if item was successfully equipped, False otherwise
        """
        if isinstance(item, Weapon):
            self.equipment['weapon'] = item
            return True
        elif isinstance(item, Armor):
            self.equipment['armor'] = item
            return True
        return False

    def use_consumable(self, item: Consumable) -> bool:
        """
        Use a consumable item.
        
        Args:
            item: The consumable item to use
            
        Returns:
            True if item was successfully used, False otherwise
        """
        if item.name in self.items and isinstance(item, Consumable):
            if self.remove_item(item.name, 1):
                return True
        return False

    def get_total_value(self) -> int:
        """
        Calculate the total value of all items in the inventory.
        
        Returns:
            Total value of all items
        """
        total = self.gold
        for item, quantity in self.items.items():
            total += item.value * quantity
        return total
