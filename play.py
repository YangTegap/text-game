#!/usr/bin/env python3
"""
GUI Launcher for The Forgotten Mansion.
Launches the graphical interface version of the game.

For terminal mode, run: python main.py
"""

import sys


def main():
    """Launch GUI mode."""
    try:
        from game_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print("\n" + "=" * 60)
        print("ERROR: GUI mode could not start")
        print("=" * 60)
        print(f"\nDetails: {e}")
        print("\nGUI mode requires tkinter (usually included with Python).")
        print("\nTo install tkinter:")
        print("  - Windows: Reinstall Python from python.org (check tcl/tk option)")
        print("  - Mac: brew install python-tk")
        print("  - Linux (Ubuntu/Debian): sudo apt-get install python3-tk")
        print("  - Linux (Fedora): sudo dnf install python3-tkinter")
        print("\nAlternatively, you can play in terminal mode:")
        print("  python main.py")
        print()
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
