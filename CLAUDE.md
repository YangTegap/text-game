# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Forgotten Mansion is a text-based adventure game that combines natural language parsing with strict rule-based world validation. The key design principle: players can phrase commands naturally, but can only interact with objects that actually exist in the game world (no AI-generated content).

## Development Commands

### Running the Game
```bash
# GUI mode (recommended for users)
python play.py

# Terminal mode (classic experience)
python main.py

# Direct GUI launch
python game_gui.py
```

### Testing
```bash
# Run all tests
python test_game.py

# The test suite validates:
# - Parser handles all command variations
# - Game state management works correctly
# - Puzzle mechanics function properly
# - Invalid commands are rejected
# - GUI imports successfully (warns if tkinter missing)
```

### File Structure
- Entry points: `play.py` (GUI launcher), `main.py` (terminal), `game_gui.py` (direct GUI)
- Core engine: `game_engine.py` (coordinates everything)
- Game systems: `parser.py`, `game_state.py`, `game_logic.py`, `world.py`
- Tests: `test_game.py`
- Documentation: `README.md`, `GUI_GUIDE.md`, `WALKTHROUGH.md`

## Architecture: The Data Flow

The game follows a strict unidirectional data flow that enforces world constraints:

```
User Input → Parser → Validator → Game Logic → Game State → Response
```

### 1. Parser (parser.py)
- Converts natural language to structured commands: `{'action': 'take', 'target': 'knife', 'secondary': None}`
- Handles 50+ synonyms per action ("take" = "get" = "pick up" = "grab")
- Extracts multi-word phrases ("pick up") before single words
- Special case: "go north" becomes just "north" action with no target
- Returns 'unknown' action for unrecognized input

### 2. Validator (parser.py: CommandValidator)
- **Critical**: Validates commands against actual game state BEFORE execution
- Checks if objects exist in current room or inventory
- Verifies exits are valid from current room
- Returns `(is_valid, error_message)` tuple
- Prevents "AI manipulation" - you can't reference non-existent objects

### 3. Game Logic (game_logic.py)
- Only executes validated commands
- Each action has a handler (e.g., `take()`, `use()`, `search()`)
- Special logic for puzzles (e.g., using stone on padlock, searching desk reveals key)
- Modifies game state through GameState API

### 4. Game State (game_state.py)
- Single source of truth for world state
- Tracks: current_room_id, inventory, flags (puzzle states), turns, score
- Provides APIs: `is_in_inventory()`, `is_in_current_room()`, `get_object_anywhere()`
- **Important**: World data is mutable - objects move from rooms to inventory
- Save/load serializes entire state including modified world

### 5. World Definition (world.py)
- `get_world_data()` returns complete world structure
- Rooms have: name, description, exits, objects
- Objects have: name, aliases, description, takeable, visible, interactions, room_description
- Exits can be simple strings or dicts with `locked`, `locked_message`, `destination`
- **Key insight**: This is where ALL content lives - parser/logic are generic

## Adding Content

### Adding a New Room
Edit `world.py` in the `rooms` dictionary:
```python
'new_room_id': {
    'name': 'Display Name',
    'description': 'What player sees',
    'exits': {
        'north': 'other_room_id',
        'east': {'destination': 'locked_room', 'locked': True, 'locked_message': 'The door is locked.'}
    },
    'objects': [...]
}
```

### Adding a New Object
```python
{
    'name': 'primary_name',  # Used in inventory
    'aliases': ['alt1', 'alt2'],  # Parser matches these too
    'description': 'Shown when examining',
    'takeable': True,  # Can be picked up?
    'visible': True,  # Shows in room description?
    'room_description': 'A key lies here.',  # How it appears in room
    'interactions': {
        'read': 'Response when player reads it',
        'search': 'Response when player searches it',
        'use': 'Response when player uses it'
    },
    'points': 10  # Added to score when taken (optional)
}
```

### Adding a New Command
1. Add synonyms to `parser.py` in `action_synonyms` dict
2. Add handler method to `game_logic.py` (e.g., `def new_action(self, target):`)
3. Wire it in `execute_command()` handlers dict
4. Update help text in `parser.py: get_help_text()`

### Adding a Puzzle
Puzzles are implemented in `game_logic.py` with special case handling:

1. **Search reveals item**: Check flag, add object to room via `state.add_object_to_room()`
2. **Use item on target**: Check conditions, modify state, unlock exits
3. **Unlock door**: Use `state.unlock_exit(direction)`
4. **Track state**: Use `state.set_flag('flag_name', True)` and `state.get_flag('flag_name')`

Example from code:
```python
# In search() method
if 'silver key' in result.lower() and target == 'desk':
    if not self.state.get_flag('desk_searched'):
        self.state.set_flag('desk_searched', True)
        self.state.add_object_to_room({...key object...})
```

## Important Design Decisions

### Parser Match Priority
1. Multi-word synonyms first ("pick up" before "pick")
2. Longest to shortest to avoid partial matches
3. Direction shortcuts (n/s/e/w) handled specially
4. "go [direction]" converted to just direction action

### Object Matching
Objects match if query equals name OR any alias (case-insensitive, trimmed). The `_matches_object()` method in GameState is used consistently.

### Validation vs Execution Separation
Commands are validated BEFORE execution. This means:
- Parser never modifies state
- Validator never modifies state
- Only GameLogic modifies state
- This makes testing easier and prevents invalid states

### GUI Threading
GUI runs game in main thread (not background thread despite `threading` import - that was for potential async operations). UI stays responsive because tkinter handles events.

### Save File Format
JSON with complete state snapshot including modified world. This means:
- Save files contain current room contents (items removed when taken)
- Flags preserve puzzle states
- Can be edited by hand if needed (it's human-readable JSON)

## Common Development Patterns

### Adding Interactive Object Behavior
Objects support these interaction keys: `read`, `search`, `use`, `open`, `close`, `push`, `pull`, `turn`, `eat`, `drink`. Add responses in world.py object definition.

### Special Use Cases
For complex "use" logic (keys, stone on padlock), add special case in `game_logic.py: use()` method before generic interaction check.

### Testing New Content
1. Add test case in `test_game.py`
2. Run `python test_game.py` to verify
3. Test interactively via `python main.py` or `python game_gui.py`

## Dual Mode Architecture

Terminal and GUI share the same game engine:
- `game_engine.py` contains game loop and command processing
- `main.py` uses it with `input()` for terminal
- `game_gui.py` uses it with tkinter for GUI
- Both produce identical gameplay

GUI specifics:
- `TerminalGUI` class wraps GameEngine
- Command history stored in `command_history` list
- Output uses tags for colored text
- Menu bar uses GameEngine methods (save_game, load_game)

## World State Consistency

Key invariant: An object exists in exactly ONE place:
- In a room's `objects` list, OR
- In player's `inventory` list, OR
- Not in the game at all (consumed or removed)

Taking an item: removes from room, adds to inventory
Dropping an item: removes from inventory, adds to current room
Searching reveals item: adds new object to room (not in any room before)

## Dependencies

- Python 3.6+ (no type hints used for broader compatibility)
- tkinter (for GUI mode only - gracefully degrades to terminal if missing)
- No external packages required (pip install not needed)
