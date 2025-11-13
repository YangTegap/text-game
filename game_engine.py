"""
Main game engine - coordinates all game systems and runs the game loop.
"""

import json
import os
from typing import Optional

from parser import Parser, CommandValidator
from game_state import GameState
from game_logic import GameLogic
from world import get_world_data


class GameEngine:
    """Main game engine that coordinates all systems."""

    def __init__(self):
        self.parser = Parser()
        self.state = None
        self.validator = None
        self.logic = None
        self.running = False
        self.save_file = 'savegame.json'

    def new_game(self):
        """Start a new game."""
        world_data = get_world_data()
        self.state = GameState(world_data)
        self.validator = CommandValidator(self.state)
        self.logic = GameLogic(self.state)
        self.running = True

        # Show intro
        self.show_intro()

        # Show starting room
        return self.state.get_room_description()

    def show_intro(self):
        """Display game introduction."""
        intro = """
╔══════════════════════════════════════════════════════════════════════╗
║                      THE FORGOTTEN MANSION                           ║
║                   A Text Adventure Game                              ║
╚══════════════════════════════════════════════════════════════════════╝

You've heard the legends of the old mansion in the forest - tales of
hidden treasures and dark secrets. Your journal hints at mysteries
waiting to be uncovered. Today, you've decided to investigate.

Your goal: Explore the mansion and discover its secrets. Perhaps you'll
find the legendary treasure that's said to be hidden within...

Type 'help' for a list of commands, or just start exploring!
Type 'quit' to exit the game at any time.

═══════════════════════════════════════════════════════════════════════
"""
        print(intro)

    def process_command(self, user_input: str) -> Optional[str]:
        """
        Process a command from the player.
        Returns the response message, or None if the game should quit.
        """
        if not user_input.strip():
            return ""

        # Parse the command
        parsed = self.parser.parse(user_input)

        # Handle special meta commands first
        if parsed['action'] == 'help':
            return self.parser.get_help_text()

        if parsed['action'] == 'quit':
            return self._handle_quit()

        if parsed['action'] == 'save':
            return self.save_game()

        if parsed['action'] == 'load':
            return self.load_game()

        if parsed['action'] == 'restart':
            return self._handle_restart()

        # Validate the command
        valid, error_msg = self.validator.validate_command(parsed)
        if not valid:
            return error_msg

        # Execute the command
        result = self.logic.execute_command(parsed)

        # Check for win condition
        if self._check_win_condition():
            return result + "\n\n" + self._show_victory()

        return result

    def _handle_quit(self) -> str:
        """Handle quit command."""
        self.running = False
        return None  # Signal to quit

    def _handle_restart(self) -> str:
        """Handle restart command."""
        response = "Are you sure you want to restart? (yes/no): "
        # This is a simplified version; in practice you'd want to handle confirmation
        self.new_game()
        return "Game restarted.\n\n" + self.state.get_room_description()

    def _check_win_condition(self) -> bool:
        """Check if the player has won."""
        # Win condition: have the golden amulet in inventory
        return self.state.is_in_inventory('golden amulet')

    def _show_victory(self) -> str:
        """Show victory message."""
        victory = """
╔══════════════════════════════════════════════════════════════════════╗
║                      CONGRATULATIONS!                                ║
╚══════════════════════════════════════════════════════════════════════╝

You've found the legendary golden amulet! The treasure of the Forgotten
Mansion is yours!

The secrets of the mansion have been revealed, and you've proven yourself
a worthy adventurer.

FINAL SCORE: {score} points
TURNS TAKEN: {turns}

Thank you for playing!
═══════════════════════════════════════════════════════════════════════
""".format(score=self.state.score, turns=self.state.turns)

        self.running = False
        return victory

    def save_game(self) -> str:
        """Save the game state to a file."""
        try:
            save_data = self.state.save_to_dict()
            with open(self.save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            return f"Game saved to {self.save_file}."
        except Exception as e:
            return f"Error saving game: {e}"

    def load_game(self) -> str:
        """Load a saved game."""
        if not os.path.exists(self.save_file):
            return f"No save file found ({self.save_file})."

        try:
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)

            self.state = GameState.load_from_dict(save_data)
            self.validator = CommandValidator(self.state)
            self.logic = GameLogic(self.state)
            self.running = True

            return "Game loaded successfully.\n\n" + self.state.get_room_description()
        except Exception as e:
            return f"Error loading game: {e}"

    def run(self):
        """Main game loop."""
        # Start new game
        initial_message = self.new_game()
        print(initial_message)
        print()

        # Main loop
        while self.running:
            try:
                # Get player input
                user_input = input("> ").strip()

                if not user_input:
                    continue

                # Process command
                response = self.process_command(user_input)

                # Check if we should quit
                if response is None:
                    print("\nThanks for playing!")
                    break

                # Show response
                if response:
                    print()
                    print(response)
                    print()

            except KeyboardInterrupt:
                print("\n\nGame interrupted.")
                confirm = input("Do you want to save before quitting? (yes/no): ").strip().lower()
                if confirm in ['yes', 'y']:
                    print(self.save_game())
                print("Thanks for playing!")
                break
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                print("Please try again, or type 'quit' to exit.")
                import traceback
                traceback.print_exc()


def main():
    """Entry point for the game."""
    engine = GameEngine()
    engine.run()


if __name__ == '__main__':
    main()
