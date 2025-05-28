"""
Sidekick module for the RPG game.

This module contains the Sidekick class, which represents companion characters.
"""
import sys
import os
from typing import Optional

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rpg_game.character import Character
from rpg_game.game_logger import GameLogger

class Sidekick(Character):
    """
    Represents a companion character that can assist the player.
    
    Inherits from Character and adds sidekick-specific behavior.
    """
    
    def __init__(
        self, 
        name: str, 
        health: int, 
        damage: int,
        weapon_name: Optional[str] = None,
        weapon_damage: int = 0,
        support_ability: str = "Heal"
    ) -> None:
        """
        Initialize a new Sidekick.
        
        Args:
            name: The sidekick's name
            health: The sidekick's initial health
            damage: The sidekick's base damage
            weapon_name: The name of the sidekick's weapon (optional)
            weapon_damage: The damage bonus of the sidekick's weapon
            support_ability: The sidekick's support ability
        """
        super().__init__(name, health, damage, weapon_name, weapon_damage)
        self.support_ability = support_ability
        self.is_boss = False
        self.is_sidekick = True

    def use_support_ability(self, target: Character, logger: GameLogger) -> None:
        """
        Use the sidekick's support ability on a target.
        
        Args:
            target: The character to support
            logger: GameLogger instance for logging
        """
        if self.support_ability.lower() == "heal":
            # Healing Spirit has a fixed heal amount of 15 as per its description
            heal_amount = 15 if self.name == "Healing Spirit" else (self.damage // 2)
            target_health = target.get_health() + heal_amount
            max_health = getattr(target, '_max_health', float('inf'))
            actual_heal = min(heal_amount, max_health - target.get_health())
            
            if actual_heal > 0:
                target.set_health(target_health)
                logger.log_combat(self, target, -actual_heal, ability=self.support_ability)
                print(f"{self.name} uses {self.support_ability} on {target.name}! Restored {actual_heal} HP.")
            else:
                print(f"{target.name} is already at full health!")
        else:
            print(f"{self.name} can't use {self.support_ability}!")

    def attack(self, target: Character, logger: GameLogger) -> int:
        """
        Perform an attack on another character.
        
        Args:
            target: The character to attack
            logger: GameLogger instance for combat logging
            
        Returns:
            The total damage dealt
        """
        # Sidekicks do 75% damage compared to normal attacks
        reduced_damage = int(self.damage * 0.75)
        total_damage = self.calculate_damage(reduced_damage)
        target.take_damage(total_damage)
        logger.log_combat(self, target, total_damage)
        return total_damage
