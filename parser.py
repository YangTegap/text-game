"""
Robust command parser for text adventure game.
Handles natural language input with synonym support and validates against game world.
"""

import re
from typing import List, Tuple, Optional, Dict, Set


class Parser:
    """Parses player commands and validates them against the game world."""

    def __init__(self):
        # Action synonyms - maps various phrasings to standard actions
        self.action_synonyms = {
            # Movement
            'go': ['go', 'walk', 'run', 'move', 'travel', 'head'],
            'north': ['north', 'n'],
            'south': ['south', 's'],
            'east': ['east', 'e'],
            'west': ['west', 'w'],
            'up': ['up', 'u', 'climb up', 'ascend'],
            'down': ['down', 'd', 'climb down', 'descend'],

            # Observation
            'look': ['look', 'l', 'examine', 'inspect', 'observe', 'check', 'view', 'study', 'see'],
            'read': ['read', 'peruse'],
            'search': ['search', 'rummage', 'dig through'],
            'listen': ['listen', 'hear'],
            'smell': ['smell', 'sniff'],

            # Manipulation
            'take': ['take', 'get', 'grab', 'pick up', 'acquire', 'obtain', 'collect'],
            'drop': ['drop', 'put down', 'discard', 'leave'],
            'use': ['use', 'utilize', 'employ'],
            'open': ['open', 'unlock'],
            'close': ['close', 'shut'],
            'push': ['push', 'press', 'shove'],
            'pull': ['pull', 'tug', 'yank'],
            'turn': ['turn', 'rotate', 'twist'],
            'eat': ['eat', 'consume', 'devour'],
            'drink': ['drink', 'sip', 'gulp'],

            # Interaction
            'talk': ['talk', 'speak', 'chat', 'converse', 'say'],
            'give': ['give', 'offer', 'hand', 'present'],
            'show': ['show', 'display', 'present'],
            'ask': ['ask', 'inquire', 'question'],
            'tell': ['tell', 'inform'],

            # Combat/Conflict
            'attack': ['attack', 'hit', 'strike', 'fight', 'kill', 'punch', 'kick'],
            'throw': ['throw', 'toss', 'hurl', 'chuck'],

            # Inventory
            'inventory': ['inventory', 'i', 'inv', 'items', 'carrying', 'what am i carrying'],

            # Meta
            'help': ['help', 'h', '?', 'commands'],
            'quit': ['quit', 'exit', 'q', 'bye', 'goodbye'],
            'save': ['save'],
            'load': ['load', 'restore'],
            'wait': ['wait', 'z'],
            'restart': ['restart', 'reset'],
        }

        # Build reverse lookup
        self.synonym_to_action = {}
        for action, synonyms in self.action_synonyms.items():
            for synonym in synonyms:
                self.synonym_to_action[synonym.lower()] = action

        # Prepositions to filter out for cleaner parsing
        self.prepositions = {
            'at', 'to', 'in', 'into', 'on', 'onto', 'with', 'from',
            'the', 'a', 'an', 'some', 'my'
        }

        # Direction words
        self.directions = {'north', 'south', 'east', 'west', 'up', 'down', 'n', 's', 'e', 'w', 'u', 'd'}

    def parse(self, input_text: str) -> Dict[str, any]:
        """
        Parse player input into a structured command.

        Returns a dict with:
        - action: standardized action name
        - target: primary object of action
        - secondary: secondary object (for give, use X on Y, etc.)
        - raw: original input
        """
        if not input_text or not input_text.strip():
            return {'action': None, 'target': None, 'secondary': None, 'raw': input_text}

        original = input_text
        input_text = input_text.lower().strip()

        # Handle special cases first
        # Single-word directions
        if input_text in self.directions:
            direction = self.synonym_to_action.get(input_text, input_text)
            return {'action': direction, 'target': None, 'secondary': None, 'raw': original}

        # Check for multi-word action synonyms first (like "pick up")
        action, remainder = self._extract_action(input_text)

        if not action:
            return {'action': 'unknown', 'target': input_text, 'secondary': None, 'raw': original}

        # Parse the remainder for target and secondary objects
        target, secondary = self._extract_objects(remainder)

        # Special case: "go north" should become just "north" action
        if action == 'go' and target and target in self.directions:
            direction = self.synonym_to_action.get(target, target)
            return {'action': direction, 'target': None, 'secondary': None, 'raw': original}

        return {
            'action': action,
            'target': target,
            'secondary': secondary,
            'raw': original
        }

    def _extract_action(self, text: str) -> Tuple[Optional[str], str]:
        """Extract the action from the input text and return remaining text."""
        # Try multi-word synonyms first (longest to shortest)
        for action, synonyms in self.action_synonyms.items():
            # Sort by length descending to match longest phrases first
            sorted_synonyms = sorted(synonyms, key=len, reverse=True)
            for synonym in sorted_synonyms:
                if text.startswith(synonym + ' ') or text == synonym:
                    remainder = text[len(synonym):].strip()
                    return action, remainder

        return None, text

    def _extract_objects(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract target and secondary objects from remaining text."""
        if not text:
            return None, None

        # Look for prepositions that indicate a secondary object
        # Patterns: "use X on Y", "give X to Y", "put X in Y"
        secondary_indicators = [' on ', ' with ', ' to ', ' in ', ' into ', ' using ']

        for indicator in secondary_indicators:
            if indicator in text:
                parts = text.split(indicator, 1)
                target = self._clean_object_name(parts[0])
                secondary = self._clean_object_name(parts[1])
                return target, secondary

        # No secondary object, just clean the target
        target = self._clean_object_name(text)
        return target, None

    def _clean_object_name(self, text: str) -> Optional[str]:
        """Clean up object name by removing articles and extra whitespace."""
        if not text:
            return None

        words = text.strip().split()
        # Remove common articles and prepositions from start
        while words and words[0] in self.prepositions:
            words.pop(0)

        if not words:
            return None

        return ' '.join(words)

    def get_help_text(self) -> str:
        """Return help text showing available commands."""
        return """
AVAILABLE COMMANDS:
==================

MOVEMENT:
  north/south/east/west (or n/s/e/w) - Move in a direction
  up/down - Climb or descend
  go [direction] - Alternative movement syntax

OBSERVATION:
  look / look at [object] - Examine your surroundings or an object
  read [object] - Read written text
  search [object] - Search inside or around something
  inventory (or i) - Check what you're carrying
  listen - Listen to your surroundings
  smell - Smell your surroundings

INTERACTION:
  take [object] - Pick up an item
  drop [object] - Drop an item
  use [object] - Use an item
  use [object] on [target] - Use one item on another
  open [object] - Open something
  close [object] - Close something
  push/pull [object] - Push or pull something
  turn [object] - Turn or rotate something
  eat/drink [object] - Consume something

  talk to [person] - Speak with someone
  give [object] to [person] - Give an item to someone
  ask [person] about [topic] - Ask about something

OTHER:
  help - Show this help text
  save - Save your game
  load - Load a saved game
  wait - Pass time
  quit - Exit the game

TIP: You can use synonyms! For example, "pick up" = "take" = "get" = "grab"
TIP: You can only interact with objects that actually exist in the game world!
"""


class CommandValidator:
    """Validates commands against the actual game state."""

    def __init__(self, game_state):
        self.game_state = game_state

    def validate_command(self, parsed_command: Dict) -> Tuple[bool, str]:
        """
        Validate that a command can be executed in the current game state.
        Returns (is_valid, error_message)
        """
        action = parsed_command['action']
        target = parsed_command['target']
        secondary = parsed_command['secondary']

        # Actions that don't need validation
        no_validation_actions = {
            'help', 'quit', 'save', 'load', 'inventory',
            'wait', 'restart', 'look', 'listen', 'smell'
        }

        if action in no_validation_actions:
            return True, ""

        # Direction validation
        if action in {'north', 'south', 'east', 'west', 'up', 'down'}:
            return self._validate_direction(action)

        # Actions that require a target
        if not target:
            return False, f"What do you want to {action}?"

        # Validate target exists and is accessible
        if target:
            valid, msg = self._validate_object_exists(target)
            if not valid:
                return False, msg

        if secondary:
            valid, msg = self._validate_object_exists(secondary)
            if not valid:
                return False, f"You don't see any '{secondary}' here."

        return True, ""

    def _validate_direction(self, direction: str) -> Tuple[bool, str]:
        """Check if the direction is valid from current room."""
        current_room = self.game_state.get_current_room()
        if not current_room:
            return False, "You seem to be nowhere. This is a bug!"

        exits = current_room.get('exits', {})
        if direction not in exits:
            return False, f"You can't go {direction} from here."

        # Check if exit is locked or blocked
        exit_info = exits[direction]
        if isinstance(exit_info, dict):
            if exit_info.get('locked', False):
                message = exit_info.get('locked_message', f"The way {direction} is locked.")
                return False, message

        return True, ""

    def _validate_object_exists(self, object_name: str) -> Tuple[bool, str]:
        """Check if an object exists in current room or inventory."""
        # Check inventory
        if self.game_state.is_in_inventory(object_name):
            return True, ""

        # Check current room
        if self.game_state.is_in_current_room(object_name):
            return True, ""

        return False, f"You don't see any '{object_name}' here."
