"""
Main entry point for the RPG game.
"""
import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now we can use absolute imports
from rpg_game.game import Game


def main() -> None:
    """Run the RPG game."""
    try:
        print("\n[DEBUG] Creating Game instance...")
        game = Game()
        print("[DEBUG] Starting game...")
        game.run()
    except Exception as e:
        print(f"\n[ERROR] An error occurred: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
