# The Forgotten Mansion

A classic-style text adventure game with a robust parser and rich interactive world.

## Features

### What Makes This Game Special

This game addresses the exact problem you described - it combines the **freedom** of natural language input with the **constraints** of a real game world:

✅ **Robust Parser** - Understands multiple ways to phrase commands
- "take knife" = "get knife" = "pick up knife" = "grab knife"
- "go north" = "north" = "n" = "walk north"
- Dozens of synonyms for every action

✅ **Rule-Based Validation** - You can only interact with what actually exists
- Can't conjure items out of thin air
- Can't manipulate objects that aren't in the game world
- Actions are validated against actual game state

✅ **Rich Interactive World**
- Multiple interconnected rooms to explore
- Dozens of interactive objects with unique behaviors
- Puzzles that require actual problem-solving
- Hidden items and secrets to discover

✅ **Classic Adventure Mechanics**
- Inventory management
- Object manipulation (take, drop, use, examine)
- Environmental interactions (search, read, open, close)
- Locked areas requiring keys or solutions

## Installation & Running

### Requirements
- Python 3.6 or higher (no external dependencies!)
- tkinter (for GUI mode - usually included with Python)

### Running the Game

**Option 1: GUI Mode (Recommended for Most Users)**

Launch the graphical interface version:

```bash
python play.py
```

Or double-click:
- **Windows**: `play.vbs` (no console window!)
- **Mac/Linux**: `play.sh` (or right-click → "Open With" → Terminal)

This launches the GUI window with the terminal-style interface - perfect for players who want a user-friendly experience!

**Option 2: Terminal Mode (For Command-Line Enthusiasts)**

For the classic command-line experience:

```bash
python main.py
```

Or:
```bash
python game_engine.py
```

Or make it executable:
```bash
chmod +x main.py
./main.py
```

**Option 3: Direct GUI Launch (Alternative)**

You can also launch the GUI directly:

```bash
python game_gui.py
```

Or:
```bash
chmod +x game_gui.py
./game_gui.py
```

### GUI Mode Features

The GUI version provides a user-friendly graphical interface that looks like a classic terminal:

- **Retro Terminal Look** - Dark background with green/cyan text
- **Easy to Use** - No need to know how terminals work
- **Menu Bar** - New Game, Save, Load, and Help options
- **Command History** - Use Up/Down arrow keys to recall previous commands
- **Adjustable Font Size** - View menu to increase/decrease text size
- **Mouse Support** - Scroll through game history with mouse wheel
- **Cross-Platform** - Works on Windows, Mac, and Linux

Perfect for players who aren't comfortable with command-line interfaces!

## How to Play

### Basic Commands

#### Movement
- `north`, `south`, `east`, `west` (or `n`, `s`, `e`, `w`)
- `up`, `down`
- `go [direction]`

#### Observation
- `look` - Examine your surroundings
- `look at [object]` - Examine something specific
- `read [object]` - Read written text
- `search [object]` - Search inside/around something
- `inventory` or `i` - Check what you're carrying

#### Manipulation
- `take [object]` - Pick up an item
- `drop [object]` - Drop an item
- `use [object]` - Use an item
- `use [object] on [target]` - Use one item on another
- `open [object]` - Open something
- `close [object]` - Close something

#### Meta Commands
- `help` - Show command list
- `save` - Save your progress
- `load` - Load a saved game
- `quit` - Exit the game

### Tips for Playing

1. **Explore thoroughly** - Search everything! Objects often contain hidden items.

2. **Read everything** - Notes, journals, and books contain important clues.

3. **Try different synonyms** - The parser understands many phrasings:
   - "examine painting" = "look at painting" = "inspect painting"
   - "pick up key" = "take key" = "get key"

4. **Objects must exist** - Unlike AI-driven games, you can only interact with objects that are actually in the game world. If you try to use something that doesn't exist, the game will tell you.

5. **Pay attention to descriptions** - The game will tell you what's in each room. If something isn't mentioned, it's not there!

6. **Solve puzzles logically** - Puzzles require actual items and actions from the game world. You can't just describe your way past obstacles.

## Game World Overview

The game world consists of several areas:

- **Your House** - Where you start. Contains useful items for your adventure.
- **The Garden** - Outside your home, leading to the forest.
- **The Forest** - A path through the woods to the mansion.
- **The Mansion Grounds** - Gated entrance to the mysterious mansion.
- **The Mansion Interior** - Multiple rooms filled with secrets and treasures.

## Puzzles & Objectives

The main objective is to explore the mansion and discover its legendary treasure. Along the way, you'll need to:

- Find ways past locked doors and gates
- Discover hidden items
- Solve environmental puzzles
- Piece together clues from various sources

## Architecture

The game is built with a modular architecture:

### Core Components

**parser.py** - Natural language parsing
- Converts player input into structured commands
- Handles synonyms and variations
- Validates commands against game state

**game_state.py** - State management
- Tracks player location and inventory
- Manages world state and flags
- Handles save/load functionality

**world.py** - World definition
- All rooms, objects, and their properties
- Descriptions and interactions
- Puzzle logic and triggers

**game_logic.py** - Action handlers
- Processes all player actions
- Implements game mechanics
- Manages puzzle solutions

**game_engine.py** - Main game loop
- Coordinates all systems
- Handles user interaction
- Win/lose conditions

**main.py** - Terminal mode entry point
- Command-line interface version
- Classic text adventure experience

**game_gui.py** - GUI mode entry point
- Graphical window interface
- Terminal-style look with modern convenience
- Menu-driven save/load
- Command history with arrow keys

**play.py** - GUI launcher
- Directly launches the GUI mode
- User-friendly entry point (recommended for most users)

## Extending the Game

Want to add your own content? The modular design makes it easy:

### Adding New Rooms

Edit `world.py` and add to the `rooms` dictionary:

```python
'new_room': {
    'name': 'Room Name',
    'description': 'What the player sees',
    'exits': {
        'north': 'other_room_id'
    },
    'objects': [...]
}
```

### Adding New Objects

Objects can have various properties:

```python
{
    'name': 'object_name',
    'aliases': ['synonym1', 'synonym2'],
    'description': 'What you see when examining it',
    'takeable': True,  # Can it be picked up?
    'visible': True,  # Shown in room description?
    'room_description': 'How it appears in the room',
    'interactions': {
        'read': 'What happens when you read it',
        'use': 'What happens when you use it',
        'search': 'What you find when searching it'
    }
}
```

### Adding New Commands

1. Add synonyms to `parser.py`
2. Add handler to `game_logic.py`
3. Wire it up in the `execute_command` method

## Design Philosophy

This game was designed to capture the best of both worlds:

**From Classic Text Adventures:**
- Rigorous world simulation
- Real puzzles with real solutions
- Constraint-based gameplay
- The satisfaction of figuring things out

**Modern Improvements:**
- Natural language parsing (not "VERB NOUN" only)
- Extensive synonym support
- Forgiving input handling
- Rich descriptions

**What It Deliberately DOESN'T Do:**
- ❌ Accept inputs for objects that don't exist
- ❌ Generate content on the fly
- ❌ Let you "describe" your way past obstacles
- ❌ Change the story based on what you type

This is intentional! The constraints make the game feel real and the victories feel earned.

## Example Session

```
> look
Your Bedroom
============
You wake up in your small but cozy bedroom...
Your journal lies on the bedside table.
Exits: north

> take journal
Taken: journal

> read journal
The last entry reads: "The old mansion holds secrets..."

> north
Hallway
=======
A narrow hallway with worn wooden floorboards...

> west
Kitchen
=======
A small, cluttered kitchen...
A kitchen knife sits on the counter.

> take knife
Taken: knife

> inventory
You are carrying:
journal, knife
```

## Save Files

Save files are stored as `savegame.json` in the game directory. They're human-readable JSON and contain your complete game state.

## Additional Documentation

- **GUI_GUIDE.md** - Complete guide to using the graphical interface mode
  - How to start GUI mode
  - Interface overview
  - Features and keyboard shortcuts
  - Troubleshooting GUI-specific issues

- **WALKTHROUGH.md** - Complete solution guide (spoilers!)
  - Step-by-step puzzle solutions
  - Item locations
  - Speedrun guide
  - Easter eggs

## Troubleshooting

**"You don't see any 'X' here"** - That object doesn't exist in your current location. Try looking around first to see what's available.

**"You can't go [direction] from here"** - That exit doesn't exist from this room. Check the exits listed in the room description.

**"What do you want to [action]?"** - The command requires a target object. For example, use "take knife" instead of just "take".

## Credits

Built with Python. No external dependencies required.

Designed to be a pure, constraint-based text adventure in the spirit of Zork, Adventure, and other classics - with modern natural language understanding.

---

Enjoy your adventure in The Forgotten Mansion! 🏚️
