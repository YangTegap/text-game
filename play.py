#!/usr/bin/env python3
"""
Launcher for The Forgotten Mansion.
Allows user to choose between terminal or GUI version.
"""

import sys


def main():
    """Main launcher."""
    print()
    print("=" * 60)
    print("          THE FORGOTTEN MANSION - LAUNCHER")
    print("=" * 60)
    print()
    print("How would you like to play?")
    print()
    print("  1. Terminal Mode (classic command-line)")
    print("  2. GUI Mode (graphical window)")
    print("  3. Exit")
    print()

    while True:
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            print("\nLaunching terminal mode...")
            print()
            from game_engine import main as terminal_main
            terminal_main()
            break
        elif choice == "2":
            print("\nLaunching GUI mode...")
            try:
                from game_gui import main as gui_main
                gui_main()
            except ImportError as e:
                print(f"\nError: Could not launch GUI mode.")
                print(f"Details: {e}")
                print("\nGUI mode requires tkinter (usually included with Python).")
                print("Try running in terminal mode instead.")
            break
        elif choice == "3":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == '__main__':
    main()
