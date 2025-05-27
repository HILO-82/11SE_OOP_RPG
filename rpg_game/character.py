"""
Character module for the RPG game.

This module contains the Character base class and the Boss subclass.
"""
import sys
import os
from typing import Optional, Union

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rpg_game.weapon import Weapon
from rpg_game.game_logger import GameLogger


class Character:
    """
    Represents a game character with health, damage, and weapon attributes.
    
    This class demonstrates encapsulation with private attributes and getter/setter methods.
    """
    
    def __init__(
        self, 
        name: str, 
        health: int, 
        damage: int, 
        weapon_name: Optional[str] = None, 
        weapon_damage: int = 0,
        level: int = 1,
        experience: int = 0,
        debug_mode: bool = False
    ) -> None:
        """
        Initialize a new Character.
        
        Args:
            name: The character's name
            health: The character's initial health
            damage: The character's base damage
            weapon_name: The name of the character's weapon (optional)
            weapon_damage: The damage bonus of the character's weapon
            level: The character's current level
            experience: The character's current experience points
            debug_mode: Whether to enable debug logging
        """
        self.name = name
        self._health = health  # Private attribute
        self.damage = damage
        self.weapon = Weapon(weapon_name, weapon_damage) if weapon_name else None
        self.is_boss = False
        self.level = level
        self.experience = experience
        self.experience_to_next_level = self.calculate_experience_to_next_level()
        self.debug_mode = debug_mode

    def calculate_experience_to_next_level(self) -> int:
        """
        Calculate the experience needed to reach the next level.
        
        Returns:
            Experience points needed for next level
        """
        return 100 * self.level  # Simple experience curve: 100 * level

    def gain_experience(self, amount: int) -> bool:
        """
        Gain experience points and potentially level up.
        
        Args:
            amount: Amount of experience to gain
            
        Returns:
            True if leveled up, False otherwise
        """
        self.experience += amount
        if self.experience >= self.experience_to_next_level:
            self.level_up()
            return True
        return False

    def level_up(self) -> None:
        """
        Level up the character, increasing stats and resetting experience.
        """
        self.level += 1
        self._health = int(self._health * 1.2)  # Increase health by 20%
        self.damage = int(self.damage * 1.2)    # Increase damage by 20%
        self.experience = 0
        self.experience_to_next_level = self.calculate_experience_to_next_level()
        print(f"\n🎉 {self.name} has leveled up to level {self.level}! 🎉")
        print(f"Health increased to {self._health}")
        print(f"Damage increased to {self.damage}")

    def get_level(self) -> int:
        """Get the character's current level."""
        return self.level

    def get_experience(self) -> int:
        """Get the character's current experience points."""
        return self.experience

    def get_experience_to_next_level(self) -> int:
        """Get the experience points needed to reach the next level."""
        return self.experience_to_next_level - self.experience

    def display(self) -> None:
        """
        Display the character's information.
        """
        weapon_name = self.weapon.name if self.weapon else 'No Weapon'
        weapon_damage = self.weapon.damage_bonus if self.weapon else 0
        print(f"Name: {self.name}")
        print(f"Level: {self.level}")
        print(f"Experience: {self.experience}/{self.experience_to_next_level}")
        print(f"Health: {self.get_health()}")
        print(f"Damage: {self.damage}")
        print(f"Weapon: {weapon_name} (+{weapon_damage} Damage)")

    def get_health(self) -> int:
        """Get the character's current health."""
        return self._health

    def set_health(self, new_health: int) -> None:
        """
        Set the character's health.
        
        Args:
            new_health: The new health value
        """
        self._health = max(0, new_health)

    def take_damage(self, damage: int) -> None:
        """
        Reduce the character's health by the given amount.
        
        Args:
            damage: The amount of damage to take
        """
        self.set_health(self.get_health() - damage)

    def calculate_damage(self, base_damage: int) -> int:
        """
        Calculate the total damage including weapon bonus.
        
        Args:
            base_damage: The base damage value
            
        Returns:
            The total damage including weapon bonus
        """
        if self.weapon:
            return base_damage + self.weapon.damage_bonus
        return base_damage

    def attack(self, target: 'Character', logger: GameLogger) -> int:
        """
        Perform an attack on another character.
        
        Args:
            target: The character to attack
            logger: GameLogger instance for combat logging
            
        Returns:
            The total damage dealt
        """
        # Calculate base damage plus any weapon bonus
        total_damage = self.calculate_damage(self.damage)
        
        # Log the attack
        logger.log_combat(self, target, total_damage)
        
        # Apply damage to target
        target.take_damage(total_damage)
        
        # Debug output if needed
        if hasattr(self, 'debug_mode') and self.debug_mode:
            weapon_bonus = self.weapon.damage_bonus if self.weapon else 0
            print(f"[DEBUG] {self.name} attacks {target.name} for {total_damage} damage (Base: {self.damage}, Weapon: +{weapon_bonus})")
            
        return total_damage

    def is_alive(self) -> bool:
        """Check if the character is still alive."""
        return self.get_health() > 0

    def display(self) -> None:
        """
        Display the character's information.
        """
        weapon_name = self.weapon.name if self.weapon else 'No Weapon'
        weapon_damage = self.weapon.damage_bonus if self.weapon else 0
        print(f"Name: {self.name}")
        print(f"Health: {self.get_health()}")
        print(f"Damage: {self.damage}")
        print(f"Weapon: {weapon_name} (+{weapon_damage} Damage)")

    def __str__(self) -> str:
        """
        Return a string representation of the character.
        
        Returns:
            A string containing character name and health
        """
        weapon_name = self.weapon.name if self.weapon else 'No Weapon'
        weapon_damage = self.weapon.damage_bonus if self.weapon else 0
        return f"{self.name} (Health: {self.get_health()})\nDamage: {self.damage}\nWeapon: {weapon_name} (+{weapon_damage} Damage)"
