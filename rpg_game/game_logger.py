"""
Game logger module for the RPG game.

This module contains the GameLogger class for logging game events.
"""
import datetime

class GameLogger:
    """
    Handles logging of game events, particularly combat.
    
    This class demonstrates association relationship with Game (solid line in UML).
    """
    
    def __init__(self, log_to_console: bool = True) -> None:
        """
        Initialize a new GameLogger.
        
        Args:
            log_to_console: Whether to output logs to console
        """
        self.log_to_console = log_to_console
        self.log_history = []
        
    def log_combat(self, attacker: 'Character', defender: 'Character', damage: int, ability: str = None) -> None:
        """
        Log a combat event.
        
        Args:
            attacker: The character who performed the attack/ability
            defender: The character who received the attack/ability
            damage: The amount of damage dealt (negative for healing)
            ability: Optional name of the ability used
        """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Determine if this is an attack, heal, or other ability
        if damage > 0:
            action = f"attacked {defender.name} for {damage} damage"
        elif damage < 0:
            action = f"healed {defender.name} for {-damage} health"
        else:
            action = f"used an ability on {defender.name}"
            
        # Include ability name if provided
        if ability:
            action = f"used {ability} to {action}"
        
        log_message = f"[{timestamp}] COMBAT: {attacker.name} {action}"
        
        if self.log_to_console:
            print(log_message)
        
        self.log_history.append({
            'timestamp': timestamp,
            'attacker': attacker.name,
            'defender': defender.name,
            'damage': damage,
            'ability': ability if ability else 'basic_attack'
        })
        
    def get_combat_history(self) -> list:
        """
        Get the complete combat history.
        
        Returns:
            List of all combat events
        """
        return self.log_history
