"""
Game module for the RPG game.

This module contains the Game class that manages the game flow.
"""
import sys
import os
from typing import List, Tuple, Dict, Any, Optional

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rpg_game.character import Character
from rpg_game.sidekick import Sidekick
from rpg_game.boss import Boss
from rpg_game.villain import Villain
from rpg_game.inventory import Inventory, Consumable, Armor
from rpg_game.game_logger import GameLogger
from rpg_game.constants import (
    PLAYER_INITIAL_HEALTH, PLAYER_INITIAL_DAMAGE,
    HEALING_SPIRIT, BATTLE_HOUND, SHIELD_GUARDIAN,
    GOBLIN_KING_NAME, GOBLIN_KING_HEALTH, GOBLIN_KING_DAMAGE,
    DARK_SORCERER_NAME, DARK_SORCERER_HEALTH, DARK_SORCERER_DAMAGE,
    SHADOW_KNIGHT_NAME, SHADOW_KNIGHT_HEALTH, SHADOW_KNIGHT_DAMAGE,
    WEAPON_ROCK_NAME, WEAPON_PAPER_NAME, WEAPON_SCISSORS_NAME
)
from rpg_game.utils.console import clear_screen, press_enter, print_border
from rpg_game.constants import *


class Game:
    """
    Manages the game flow, including character creation, combat, and game state.
    
    This class demonstrates orchestration of other classes and game logic.
    """
    
    def __init__(self) -> None:
        """Initialize a new Game instance."""
        self.player: Optional[Character] = None
        self.sidekicks: List[Sidekick] = []
        self.inventory = Inventory()
        self.logger = GameLogger()
        self.debug_mode = False
        self.current_boss_index = 0

    # Show the introductory message and set up the game
    def show_intro(self) -> None:
        """Display the game introduction and set up the player character."""
        if self.debug_mode:
            print("[DEBUG] In show_intro method")
        try:
            clear_screen()
            if self.debug_mode:
                print("[DEBUG] After clear_screen")
            print(WELCOME_MESSAGE)
            if self.debug_mode:
                print("[DEBUG] After WELCOME_MESSAGE")
                
            player_name = input("Enter your character's name: ").strip()
            
            # Check for debug mode
            if player_name.upper() == "DEBUG":
                self.debug_mode = True
                player_name = "DebugPlayer"
                print("\n=== DEBUG MODE ACTIVATED ===")
                print("Showing detailed game information and stats.\n")
            else:
                player_name = player_name.capitalize()
                
            if self.debug_mode:
                print(f"[DEBUG] Got player name: {player_name}")
                print("[DEBUG] Debug mode:", self.debug_mode)
                
            print(INTRO_MESSAGE.format(player_name=player_name))
            if self.debug_mode:
                print("[DEBUG] After INTRO_MESSAGE")
                
            self.setup_game(player_name)
            if self.debug_mode:
                print("[DEBUG] After setup_game")
                
        except Exception as e:
            error_msg = f"[ERROR] In show_intro: {type(e).__name__}: {str(e)}"
            print(error_msg)
            if self.debug_mode:
                import traceback
                traceback.print_exc()
            raise

    # Set up the game by creating the player character and bosses
    def setup_game(self, name: str) -> None:
        """
        Set up the game with player character, sidekicks, and bosses.
        
        Args:
            name: The player character's name
        """
        if self.debug_mode:
            print("\n[DEBUG] Setting up game...")
            # Get weapon details instead of a Weapon object
            print("[DEBUG] Choosing weapon...")
        weapon_name, weapon_damage = self.choose_weapon()
        if self.debug_mode:
            print(f"[DEBUG] Creating player with name={name}, health={PLAYER_INITIAL_HEALTH}, damage={PLAYER_INITIAL_DAMAGE}, weapon={weapon_name}, weapon_damage={weapon_damage}")
        self.player = Character(name, PLAYER_INITIAL_HEALTH, PLAYER_INITIAL_DAMAGE, 
                               weapon_name, weapon_damage, debug_mode=self.debug_mode)
        
        # Sidekick will be added after first boss is defeated
        self.sidekicks = []  # Initialize empty sidekicks list
        
        # Start with empty inventory
        if self.debug_mode:
            print("[DEBUG] Starting with empty inventory")
        
        # Display player info and chosen weapon
        print("\n=== Character Created ===")
        print(f"Name: {self.player.name}")
        print(f"Health: {self.player.get_health()}")
        print(f"Weapon: {weapon_name} (+{weapon_damage} damage)")
        
        print(f"\nYou start with nothing but your wits and your trusty {weapon_name}.")
        press_enter()
        
        # Initialize bosses
        self.bosses = [
            Boss(GOBLIN_KING_NAME, GOBLIN_KING_HEALTH, GOBLIN_KING_DAMAGE), 
            Boss(DARK_SORCERER_NAME, DARK_SORCERER_HEALTH, DARK_SORCERER_DAMAGE),
            Villain(SHADOW_KNIGHT_NAME, SHADOW_KNIGHT_HEALTH, SHADOW_KNIGHT_DAMAGE, 
                   "Dark Sword", 5, "Dark Magic")
        ]

    # Allow the player to choose a weapon
    def choose_weapon(self) -> Tuple[str, int]:
        """
        Let the player choose a starting weapon with randomized damage values.
        
        Returns:
            A tuple containing the weapon name and damage bonus
        """
        if self.debug_mode:
            print("[DEBUG] In choose_weapon method")
        
        # Base weapons with random damage between 1-5
        import random
        weapons = [
            {"name": WEAPON_ROCK_NAME, "damage_bonus": random.randint(1, 5)},
            {"name": WEAPON_PAPER_NAME, "damage_bonus": random.randint(1, 5)},
            {"name": WEAPON_SCISSORS_NAME, "damage_bonus": random.randint(1, 5)}
        ]
        
        if self.debug_mode:
            print(f"[DEBUG] Available weapons: {weapons}")
            print("[DEBUG] Prompting user for weapon choice")
            
        while True:
            print("\nChoose your weapon:")
            for i, weapon in enumerate(weapons, 1):
                if self.debug_mode:
                    print(f"{i}. {weapon['name']} (Damage: +{weapon['damage_bonus']})")
                else:
                    print(f"{i}. {weapon['name']}")
            
            choice = input("Enter your choice (name or number): ").strip().lower()
            
            # Try to match by number first
            if choice.isdigit() and 1 <= int(choice) <= len(weapons):
                weapon_data = weapons[int(choice) - 1]
            else:
                # Try to match by name (case-insensitive, partial match)
                matched_weapons = [w for w in weapons if choice in w['name'].lower()]
                if len(matched_weapons) == 1:
                    weapon_data = matched_weapons[0]
                elif len(matched_weapons) > 1:
                    print(f"Multiple weapons match '{choice}'. Please be more specific.")
                    continue
                else:
                    print(f"Invalid choice. Please enter a valid weapon name or number.")
                    continue
            
            if self.debug_mode:
                print(f"[DEBUG] User chose: {weapon_data}")
            return weapon_data["name"], weapon_data["damage_bonus"]

    # Get valid user input for weapon choice
    def get_valid_input(self, prompt: str, options: List[str]) -> str:
        """
        Get valid user input from a list of options.
        
        Args:
            prompt: The prompt to display to the user
            options: List of valid options (as strings)
            
        Returns:
            The chosen option as a string
        """
        while True:
            user_input = input(prompt).strip()
            if user_input in options:
                return user_input  # Return the string value directly
            print("Invalid input, please try again.")

    # Handle the combat between player and enemy
    def combat(self, player: Character, enemy: Boss) -> bool:
        """
        Handle combat between player and enemy.
        
        Args:
            player: The player character
            enemy: The enemy character
            
        Returns:
            True if the player won, False otherwise
        """
        while player.get_health() > 0 and enemy.get_health() > 0:
            self.display_combat_status(player, enemy)
            
            # Display combat options
            print("\nCombat Options:")
            options = []
            
            # Always available options
            print("1. Attack")
            print("2. Use Item")
            options.extend(["1", "2"])
            
            # Sidekick action only if available
            if self.sidekicks:
                print("3. Sidekick Action")
                options.append("3")
            
            # Always show inventory as the last option
            inventory_option = str(len(options) + 1)
            print(f"{inventory_option}. View Inventory")
            options.append(inventory_option)
            
            # Get and validate user choice
            choice = self.get_valid_input(f"Choose an action (1-{len(options)}): ", options)
            
            # Debug logging
            if self.debug_mode:
                print(f"[DEBUG] User chose option: {choice}")
            
            # Handle the selected action
            if choice == "1":  # Attack
                if self.debug_mode:
                    print(f"[DEBUG] Player attacking {enemy.name}")
                damage_dealt = player.attack(enemy, self.logger)
                print(f"You dealt {damage_dealt} damage to {enemy.name}.")
                
                # Check if enemy is defeated
                if enemy.get_health() <= 0:
                    self.print_victory_message(enemy)
                    # Grant experience for defeating the enemy
                    xp_gain = enemy.damage * 10  # Simple XP formula
                    print(f"\nYou gained {xp_gain} experience points!")
                    player.gain_experience(xp_gain)
                    # Add loot to inventory
                    self.add_loot(enemy)
                    return True
                
            elif choice == "2":  # Use Item
                self.use_item(player)
                press_enter()
                continue
                
            elif choice == "3" and self.sidekicks:  # Sidekick Action
                sidekick = self.sidekicks[0]  # Use the first sidekick
                sidekick.use_support_ability(player, self.logger)
                print(f"{sidekick.name} used {sidekick.support_ability}!")
                
            elif choice == inventory_option:  # View Inventory
                self.display_inventory(debug=self.debug_mode)
                press_enter()
                continue
            
            # Only proceed to enemy's turn if the enemy is still alive
            if enemy.get_health() > 0:
                damage_received = enemy.attack(player, self.logger)
                print(f"{enemy.name} dealt {damage_received} damage to you.")
                
                if player.get_health() <= 0:
                    self.print_defeat_message(enemy)
                    return False
                
                press_enter()
            else:
                press_enter()

    # Display the current status of the combat
    def display_combat_status(self, player: Character, enemy: Boss) -> None:
        """
        Display the current combat status.
        
        Args:
            player: The player character
            enemy: The enemy character
        """
        clear_screen()
        level = "LEVEL 1" if enemy.name == "Goblin King" else "LEVEL 2"
        print(f"\n=============> {level}: {enemy.name} <=============")
        
        # Player stats
        print("\n=== Player Stats ===")
        player.display()
        if self.debug_mode:
            try:
                print(f"\n[DEBUG] Player attributes:")
                print(f"- Current Health: {player.get_health() if hasattr(player, 'get_health') else 'N/A'}")
                if hasattr(player, '_max_health'):
                    print(f"- Max Health: {player._max_health}")
                elif hasattr(player, 'max_health'):
                    print(f"- Max Health: {player.max_health}")
                print(f"- Base Damage: {getattr(player, 'damage', 'N/A')}")
                if hasattr(player, 'weapon'):
                    weapon = player.weapon
                    print(f"- Weapon: {weapon.name if weapon else 'None'}")
                    if weapon and hasattr(weapon, 'damage_bonus'):
                        print(f"  - Damage Bonus: +{weapon.damage_bonus}")
            except Exception as e:
                print(f"[DEBUG ERROR] Failed to display player debug info: {e}")
        
        # Enemy stats
        print("\n=== Enemy Stats ===")
        enemy.display()
        if self.debug_mode:
            try:
                print(f"\n[DEBUG] Enemy attributes:")
                print(f"- Current Health: {enemy.get_health() if hasattr(enemy, 'get_health') else 'N/A'}")
                if hasattr(enemy, '_max_health'):
                    print(f"- Max Health: {enemy._max_health}")
                elif hasattr(enemy, 'max_health'):
                    print(f"- Max Health: {enemy.max_health}")
                print(f"- Base Damage: {getattr(enemy, 'damage', 'N/A')}")
                if hasattr(enemy, 'weapon'):
                    weapon = enemy.weapon
                    print(f"- Weapon: {weapon.name if weapon else 'None'}")
                    if weapon and hasattr(weapon, 'damage_bonus'):
                        print(f"  - Damage Bonus: +{weapon.damage_bonus}")
            except Exception as e:
                print(f"[DEBUG ERROR] Failed to display enemy debug info: {e}")
        
        # Sidekicks info
        if hasattr(self, 'sidekicks') and self.sidekicks:
            print("\n=== Sidekicks ===")
            for sidekick in self.sidekicks:
                try:
                    print(f"\n{getattr(sidekick, 'name', 'Unknown')}")
                    print(f"Health: {sidekick.get_health() if hasattr(sidekick, 'get_health') else 'N/A'}")
                    print(f"Support Ability: {getattr(sidekick, 'support_ability', 'N/A')}")
                    
                    if self.debug_mode:
                        try:
                            print("[DEBUG] Sidekick attributes:")
                            print(f"- Current Health: {sidekick.get_health() if hasattr(sidekick, 'get_health') else 'N/A'}")
                            if hasattr(sidekick, '_max_health'):
                                print(f"- Max Health: {sidekick._max_health}")
                            elif hasattr(sidekick, 'max_health'):
                                print(f"- Max Health: {sidekick.max_health}")
                            print(f"- Base Damage: {getattr(sidekick, 'damage', 'N/A')}")
                        except Exception as e:
                            print(f"[DEBUG ERROR] Failed to display sidekick debug info: {e}")
                except Exception as e:
                    print(f"[ERROR] Failed to display sidekick info: {e}")
        
        # Inventory is now only shown when the player chooses to view it
        
        if self.debug_mode:
            try:
                print("\n[DEBUG] Game State:")
                print(f"- Number of bosses remaining: {len(self.bosses) if hasattr(self, 'bosses') else 'N/A'}")
                print(f"- Current boss health: {enemy.get_health() if hasattr(enemy, 'get_health') else 'N/A'}")
                print(f"- Player health: {player.get_health() if hasattr(player, 'get_health') else 'N/A'}")
                print(f"- Sidekicks active: {len(self.sidekicks) if hasattr(self, 'sidekicks') else 0}")
            except Exception as e:
                print(f"[DEBUG ERROR] Failed to display game state: {e}")
        
        print("-" * SEPARATOR_LENGTH)

    # Introduce each boss before the battle
    def introduce_boss(self, boss: Boss) -> None:
        """
        Introduce a boss before battle.
        
        Args:
            boss: The boss to introduce
        """
        clear_screen()
        intro_messages = {
            GOBLIN_KING_NAME: GOBLIN_KING_INTRO.format(player_name=self.player.name),
            DARK_SORCERER_NAME: DARK_SORCERER_INTRO.format(player_name=self.player.name)
        }
        print(intro_messages.get(boss.name, "A new boss appears!"))
        press_enter()

    # Print victory message after defeating an enemy
    def print_victory_message(self, enemy: Boss) -> None:
        """
        Print a victory message.
        
        Args:
            enemy: The defeated enemy
        """
        print_border()
        print(VICTORY_MESSAGE.format(enemy_name=enemy.name))
        press_enter()

    # Print defeat message after being defeated by an enemy
    def print_defeat_message(self, enemy: Boss) -> None:
        """
        Print a defeat message.
        
        Args:
            enemy: The enemy that defeated the player
        """
        print_border()
        print(DEFEAT_MESSAGE.format(enemy_name=enemy.name))
        press_enter()

    # End the game and show final message
    def display_inventory(self, debug: bool = False) -> None:
        """
        Display the player's inventory.
        
        Args:
            debug: Whether to show debug information
        """
        if not debug:
            print(f"Gold: {self.inventory.gold}")
            print("\nItems:")
            if not self.inventory.items:
                print("No items in inventory")
            else:
                for item_name, item_data in self.inventory.items.items():
                    item = item_data['item']
                    quantity = item_data['quantity']
                    print(f"{item_name} x{quantity}")
            
            print("\nEquipment:")
            print(f"Weapon: {self.inventory.equipment['weapon'].name if self.inventory.equipment['weapon'] else 'None'}")
            print(f"Armor: {self.inventory.equipment['armor'].name if self.inventory.equipment['armor'] else 'None'}")
        else:
            # Debug mode inventory display
            print(f"Gold: {self.inventory.gold}")
            print("\n=== Items (Debug) ===")
            if not self.inventory.items:
                print("No items in inventory")
            else:
                for item_name, item_data in self.inventory.items.items():
                    item = item_data['item']
                    quantity = item_data['quantity']
                    print(f"{item_name} x{quantity}")
                    print(f"  - Type: {item.__class__.__name__}")
                    print(f"  - Description: {item.description}")
                    print(f"  - Value: {item.value} gold")
                    if hasattr(item, 'heal_amount'):
                        print(f"  - Heal Amount: {item.heal_amount} HP")
                    if hasattr(item, 'defense_bonus'):
                        print(f"  - Defense Bonus: +{item.defense_bonus}")
                    if hasattr(item, 'damage_bonus'):
                        print(f"  - Damage Bonus: +{item.damage_bonus}")
                    print()

    def use_item(self, character: Character) -> None:
        """
        Use an item from the inventory.
        
        Args:
            character: The character using the item
        """
        print("\nAvailable Items:")
        consumables = []
        for item_name, item_data in self.inventory.items.items():
            if isinstance(item_data['item'], Consumable):
                consumables.append(item_data['item'])
                
        if not consumables:
            print("No consumable items available!")
            return
            
        for i, item in enumerate(consumables):
            print(f"{i + 1}. {item.name} ({item.heal_amount} HP) x{self.inventory.items[item.name]['quantity']}")
        
        choice = self.get_valid_input("Choose an item to use (1-{}): ".format(len(consumables)), 
                                    [str(i + 1) for i in range(len(consumables))])
        
        if choice is not None:
            item = consumables[choice]
            if self.inventory.use_consumable(item):
                character.set_health(character.get_health() + item.heal_amount)
                print(f"Used {item.name}! Restored {item.heal_amount} HP.")
                print(f"Remaining {item.name}: {self.inventory.items[item.name]['quantity'] if item.name in self.inventory.items else 0}")
            else:
                print("Failed to use item!")

    def add_loot(self, enemy: Boss) -> None:
        """
        Add loot from defeated enemy to inventory.
        
        Args:
            enemy: The defeated enemy
        """
        # Add random gold
        gold = enemy.damage * 5
        self.inventory.gold += gold
        print(f"\nFound {gold} gold!")
        
        # Add random items
        import random
        if random.random() < 0.5:  # 50% chance to drop a health potion
            self.inventory.add_item(Consumable("Health Potion", "Restores 20 health", 10, 20))
            print("Found a Health Potion!")
        
        if random.random() < 0.3:  # 30% chance to drop armor
            defense = enemy.damage // 2
            self.inventory.add_item(Armor(f"{enemy.name}'s Armor", f"Armor dropped by {enemy.name}", 50, defense))
            print(f"Found {enemy.name}'s Armor!")

    def end_game(self, player_won: bool) -> None:
        """
        End the game and show the final message.
        
        Args:
            player_won: Whether the player won the game
        """
        print_border()
        if player_won:
            print(GAME_WIN_MESSAGE.format(player_name=self.player.name))
        else:
            print(GAME_OVER_MESSAGE.format(player_name=self.player.name))
        print_border()

    def choose_sidekick(self) -> None:
        """Let the player choose a sidekick before the second boss fight."""
        print("\n=== SIDEKICK SELECTION ===\n")
        print("Before facing the next boss, you can choose a sidekick to aid you in battle!")
        print("Each sidekick has unique abilities that can help you in different ways.\n")
        
        # Define available sidekicks
        sidekicks = [
            {
                "name": HEALING_SPIRIT["name"],
                "health": HEALING_SPIRIT["health"],
                "damage": HEALING_SPIRIT["damage"],
                "ability": HEALING_SPIRIT["ability"],
                "description": HEALING_SPIRIT["description"]
            },
            {
                "name": BATTLE_HOUND["name"],
                "health": BATTLE_HOUND["health"],
                "damage": BATTLE_HOUND["damage"],
                "ability": BATTLE_HOUND["ability"],
                "description": BATTLE_HOUND["description"]
            },
            {
                "name": SHIELD_GUARDIAN["name"],
                "health": SHIELD_GUARDIAN["health"],
                "damage": SHIELD_GUARDIAN["damage"],
                "ability": SHIELD_GUARDIAN["ability"],
                "description": SHIELD_GUARDIAN["description"]
            }
        ]
        
        # Display sidekick options
        while True:
            print("\nChoose your sidekick:")
            for i, sidekick in enumerate(sidekicks, 1):
                print(f"{i}. {sidekick['name']} - {sidekick['ability']}")
                print(f"   {sidekick['description']}")
                print(f"   Health: {sidekick['health']}, Damage: {sidekick['damage']}\n")
            
            choice = input("Enter the number of your choice (1-3): ").strip()
            
            if choice in ["1", "2", "3"]:
                selected = sidekicks[int(choice) - 1]
                from rpg_game.sidekick import Sidekick
                
                # Clear any existing sidekicks
                self.sidekicks = []
                
                # Add the selected sidekick
                self.sidekicks.append(Sidekick(
                    name=selected["name"],
                    health=selected["health"],
                    damage=selected["damage"],
                    support_ability=selected["ability"]
                ))
                
                print(f"\nYou have chosen {selected['name']} as your sidekick!")
                print(f"{selected['name']} will aid you in battle with their {selected['ability']} ability!")
                press_enter()
                return
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")

    def handle_boss_battles(self) -> None:
        """Handle the sequence of boss battles."""
        print("\n=== BOSS BATTLES BEGIN ===\n")
        
        for i, boss in enumerate(self.bosses):
            # Before the second boss, let the player choose a sidekick
            if i == 1:  # Second boss (0-based index)
                self.choose_sidekick()
            
            # Introduce the boss
            self.introduce_boss(boss)
            
            # Start the battle
            if not self.combat(self.player, boss):
                # Player lost the battle
                self.end_game(False)
                return
            
            # Player won the battle
            print(f"\nYou have defeated {boss.name}!")
            
            # Check if there are more bosses
            if boss != self.bosses[-1]:
                print("Prepare for the next battle...")
                press_enter()
        
        # All bosses defeated
        self.end_game(True)

    # Run the game
    def run(self) -> None:
        """Run the game from start to finish."""
        print("[DEBUG] In run method")
        self.show_intro()
        print("[DEBUG] After show_intro")
        self.handle_boss_battles()
        print("[DEBUG] After handle_boss_battles")
