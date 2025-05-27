"""
Boss module for the RPG game.

This module contains the Boss class, which inherits from Character.
"""
import sys
import os
from typing import Optional

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rpg_game.character import Character
from rpg_game.game_logger import GameLogger

class Boss(Character):
    """
    Represents a boss character in the game.
    
    Inherits from Character and adds boss-specific behavior.
    """
    
    def __init__(
        self, 
        name: str, 
        health: int, 
        damage: int,
        weapon_name: Optional[str] = None,
        weapon_damage: int = 0
    ) -> None:
        """
        Initialize a new Boss.
        
        Args:
            name: The boss's name
            health: The boss's initial health
            damage: The boss's base damage
            weapon_name: The name of the boss's weapon (optional)
            weapon_damage: The damage bonus of the boss's weapon
        """
        super().__init__(name, health, damage, weapon_name, weapon_damage)
        self.is_boss = True

    def special_attack(self, target: Character, logger: GameLogger) -> int:
        """
        Perform a special boss attack that deals extra damage.
        
        Args:
            target: The character to attack
            logger: GameLogger instance for combat logging
            
        Returns:
            The total damage dealt
        """
        base_damage = self.damage + (self.damage * 0.5)  # 50% bonus damage
        total_damage = self.calculate_damage(base_damage)
        target.take_damage(total_damage)
        logger.log_combat(self, target, total_damage)
        return total_damage
