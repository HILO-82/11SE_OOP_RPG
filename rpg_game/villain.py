"""
Villain module for the RPG game.

This module contains the Villain class, which represents powerful enemy characters.
"""
import sys
import os
from typing import Optional

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rpg_game.character import Character
from rpg_game.game_logger import GameLogger

class Villain(Character):
    """
    Represents a powerful enemy character with unique abilities.
    
    Inherits from Character and adds villain-specific behavior.
    """
    
    def __init__(
        self, 
        name: str, 
        health: int, 
        damage: int,
        weapon_name: Optional[str] = None,
        weapon_damage: int = 0,
        special_ability: str = "Dark Magic"
    ) -> None:
        """
        Initialize a new Villain.
        
        Args:
            name: The villain's name
            health: The villain's initial health
            damage: The villain's base damage
            weapon_name: The name of the villain's weapon (optional)
            weapon_damage: The damage bonus of the villain's weapon
            special_ability: The villain's special ability
        """
        super().__init__(name, health, damage, weapon_name, weapon_damage)
        self.special_ability = special_ability
        self.is_boss = True
        self.is_villain = True

    def use_special_ability(self, target: Character, logger: GameLogger) -> int:
        """
        Use the villain's special ability on a target.
        
        Args:
            target: The character to target
            logger: GameLogger instance for logging
            
        Returns:
            The damage dealt by the special ability
        """
        if self.special_ability.lower() == "dark magic":
            base_damage = self.damage * 2  # Villains deal double damage with special abilities
            total_damage = self.calculate_damage(base_damage)
            target.take_damage(total_damage)
            logger.log_combat(self, target, total_damage, ability=self.special_ability)
            print(f"{self.name} uses {self.special_ability} on {target.name}!")
            return total_damage
        return 0

    def attack(self, target: Character, logger: GameLogger) -> int:
        """
        Perform an attack on another character.
        
        Args:
            target: The character to attack
            logger: GameLogger instance for combat logging
            
        Returns:
            The total damage dealt
        """
        # Villains have a 20% chance to use their special ability instead of normal attack
        import random
        if random.random() < 0.2:
            return self.use_special_ability(target, logger)
            
        # Otherwise perform a normal attack with bonus damage
        bonus_damage = int(self.damage * 0.25)  # Villains deal 25% extra damage
        total_damage = self.calculate_damage(self.damage + bonus_damage)
        target.take_damage(total_damage)
        logger.log_combat(self, target, total_damage)
        return total_damage
