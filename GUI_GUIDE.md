# GUI Mode Guide

The Forgotten Mansion includes a graphical user interface (GUI) mode that provides a retro terminal-style experience in a dedicated window. This is perfect for players who want the classic text adventure feel without needing to use a command-line terminal.

## Starting GUI Mode

### Method 1: Using the Launcher (Easiest)

**Windows:**
- Double-click `play.bat`
- The GUI window will open automatically!

**Mac/Linux:**
- Double-click `play.sh` (or right-click → Open With → Terminal)
- Or run: `./play.sh` or `python play.py`
- The GUI window will open automatically!

### Method 2: Direct Launch

**Command Line:**
```bash
python game_gui.py
```

**Or on Mac/Linux:**
```bash
./game_gui.py
```

**Windows:**
- You can create a shortcut to `game_gui.py` and double-click it

## GUI Interface Overview

```
┌─────────────────────────────────────────────────────────┐
│ File  Game  View  Help                                  │ ← Menu Bar
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Your Bedroom                                            │
│  ============                                            │
│  You wake up in your small but cozy bedroom...          │
│                                                          │
│  > take journal                                          │ ← Your commands
│  Taken: journal                                          │ ← Game responses
│                                                          │
│  > north                                                 │
│  Hallway                                                 │
│  =======                                                 │
│  A narrow hallway...                                     │
│                                                          │
│  [Scrollable game history]                              │
│                                                          │
├─────────────────────────────────────────────────────────┤
│ > [Type your commands here]                             │ ← Input area
└─────────────────────────────────────────────────────────┘
```

## Features

### 1. Menu Bar

**Game Menu:**
- **New Game** - Start over (with confirmation)
- **Save Game** - Save your progress to a file
- **Load Game** - Restore a saved game
- **Exit** - Quit (with save reminder)

**View Menu:**
- **Increase Font Size** - Make text larger
- **Decrease Font Size** - Make text smaller
- **Clear Screen** - Clear the output (doesn't affect game state)

**Help Menu:**
- **Commands** - View all available game commands
- **About** - Information about the game

### 2. Terminal-Style Appearance

- **Dark Background** - Easy on the eyes, classic terminal look
- **Monospace Font** - Clear, readable "Courier New" font
- **Color Coding:**
  - Cyan `>` prompt - Shows where to type
  - Green text - Your input commands
  - Gray text - Game responses
  - Yellow text - Headers and special messages

### 3. Command History

Like a real terminal, you can navigate your command history:

- **Up Arrow ↑** - Go to previous command
- **Down Arrow ↓** - Go to next command

This makes it easy to:
- Repeat commands (like "look" to see the room again)
- Correct typos (recall the command and edit it)
- Speed up gameplay (repeat common actions)

### 4. Scrolling

- **Mouse Wheel** - Scroll through game history
- **Scrollbar** - Click and drag to navigate
- Auto-scrolls to bottom when new text appears

### 5. Keyboard Shortcuts

- **Enter** - Submit command
- **Up/Down Arrows** - Command history
- **Ctrl+A** - Select all in input field
- **Ctrl+C** - Copy selected text
- **Ctrl+V** - Paste into input field

## Tips for GUI Mode

### For New Players

1. **Just start typing!** The game tells you what you can do.
   - Type `look` to see where you are
   - Type `help` for a command list
   - Type commands like "take knife" or "go north"

2. **Use the menu** if you're not sure what to do
   - Help → Commands shows all available actions

3. **Save often!**
   - Game → Save Game (creates a file called `savegame.json`)
   - You can load it later with Game → Load Game

4. **Stuck?** Check the WALKTHROUGH.md file for hints!

### For Terminal Users

If you're comfortable with terminals, you might prefer:
- Terminal mode for the authentic experience
- GUI mode for a larger, scrollable window
- GUI mode for the menu-based save/load

Both modes play the exact same game!

## Troubleshooting

### "ModuleNotFoundError: No module named 'tkinter'"

**Problem:** tkinter is not installed

**Solutions:**

**Windows:**
- tkinter comes with Python by default
- If missing, reinstall Python from python.org and check "tcl/tk" during installation

**Mac:**
```bash
# If using system Python
# tkinter should be included

# If using Homebrew Python
brew install python-tk
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

**Linux (Fedora/Red Hat):**
```bash
sudo dnf install python3-tkinter
```

### GUI Window is Too Small/Large

Use the View menu to adjust font size:
- View → Increase Font Size (makes everything bigger)
- View → Decrease Font Size (makes everything smaller)

Or resize the window by dragging the edges/corners.

### Game Froze

This shouldn't happen, but if it does:
- Try closing and reopening the window
- Your save file is safe! Use Game → Load Game

### Text is Hard to Read

The default color scheme is:
- Background: Dark gray (#0C0C0C)
- Text: Light gray (#CCCCCC)
- Input: Green (#00FF00)
- Prompt: Cyan (#00AAFF)

These colors are chosen for readability and a classic terminal aesthetic. If you have vision difficulties, consider:
- Using terminal mode with your terminal's custom colors
- Increasing font size (View menu)

## Advantages of GUI Mode

✅ **Easier for non-technical users** - No need to know what a terminal is

✅ **Better scrolling** - Mouse wheel support, larger scrollback buffer

✅ **Menu-driven** - All functions available via menus

✅ **Command history** - Easily recall previous commands

✅ **Adjustable text size** - Works for all vision levels

✅ **Cross-platform** - Same experience on Windows, Mac, Linux

✅ **Window management** - Minimize, maximize, move around

## When to Use Terminal Mode Instead

Consider terminal mode if you:
- Prefer traditional command-line interfaces
- Want to use your terminal's custom color scheme
- Are running on a system without a graphical environment
- Want the most "authentic" text adventure experience
- Prefer a minimal interface

Both modes are equally powerful - it's just personal preference!

## Screenshots (Description)

Since this is a text game, here's what you'll see:

```
╔══════════════════════════════════════════════════════════╗
║                THE FORGOTTEN MANSION                     ║
║               A Text Adventure Game                      ║
╚══════════════════════════════════════════════════════════╝

You've heard the legends of the old mansion in the forest -
tales of hidden treasures and dark secrets. Your journal hints
at mysteries waiting to be uncovered. Today, you've decided to
investigate.

Your goal: Explore the mansion and discover its secrets.
Perhaps you'll find the legendary treasure that's said to be
hidden within...

Type 'help' for a list of commands, or just start exploring!
Type 'quit' to exit the game at any time.

═══════════════════════════════════════════════════════════
```

All of this appears in a nice graphical window with a retro terminal aesthetic!

## Have Fun!

The GUI mode is designed to make text adventures accessible to everyone, whether you're a terminal wizard or someone who's never seen a command prompt.

Explore the mansion, solve the puzzles, and find the treasure! 🏚️✨
