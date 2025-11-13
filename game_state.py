"""
Game state management - tracks player location, inventory, world state, and game progress.
"""

import json
import copy
from typing import Dict, List, Optional, Set


class GameState:
    """Manages the current state of the game."""

    def __init__(self, world_data: Dict):
        self.world = world_data
        self.current_room_id = world_data.get('start_room', 'entrance')
        self.inventory = []
        self.flags = {}  # For tracking game events (doors unlocked, puzzles solved, etc.)
        self.turns = 0
        self.score = 0
        self.visited_rooms = set()

    def get_current_room(self) -> Dict:
        """Get the current room data."""
        room = self.world['rooms'].get(self.current_room_id)
        if not room:
            raise ValueError(f"Room {self.current_room_id} not found!")
        return room

    def get_room_by_id(self, room_id: str) -> Optional[Dict]:
        """Get a room by its ID."""
        return self.world['rooms'].get(room_id)

    def move_to_room(self, room_id: str) -> bool:
        """Move player to a different room."""
        if room_id in self.world['rooms']:
            self.current_room_id = room_id
            self.visited_rooms.add(room_id)
            self.turns += 1
            return True
        return False

    def is_in_inventory(self, object_name: str) -> bool:
        """Check if an object is in player's inventory."""
        return any(self._normalize(obj) == self._normalize(object_name) for obj in self.inventory)

    def is_in_current_room(self, object_name: str) -> bool:
        """Check if an object is in the current room."""
        room = self.get_current_room()
        objects = room.get('objects', [])
        return any(self._matches_object(obj, object_name) for obj in objects)

    def get_object_from_room(self, object_name: str) -> Optional[Dict]:
        """Get object data from current room."""
        room = self.get_current_room()
        for obj in room.get('objects', []):
            if self._matches_object(obj, object_name):
                return obj
        return None

    def get_object_from_inventory(self, object_name: str) -> Optional[str]:
        """Get object from inventory."""
        for obj in self.inventory:
            if self._normalize(obj) == self._normalize(object_name):
                return obj
        return None

    def get_object_anywhere(self, object_name: str) -> Optional[Dict]:
        """Get object from current room or inventory."""
        # Check current room first
        obj = self.get_object_from_room(object_name)
        if obj:
            return obj

        # Check inventory
        if self.is_in_inventory(object_name):
            # Look up full object data from world
            return self._get_object_definition(object_name)

        return None

    def _get_object_definition(self, object_name: str) -> Optional[Dict]:
        """Get the full definition of an object from world data."""
        for room_id, room_data in self.world['rooms'].items():
            for obj in room_data.get('objects', []):
                if self._matches_object(obj, object_name):
                    return obj
        return None

    def add_to_inventory(self, object_name: str) -> bool:
        """Add object to inventory and remove from room."""
        room = self.get_current_room()
        objects = room.get('objects', [])

        for obj in objects:
            if self._matches_object(obj, object_name):
                # Check if object is takeable
                if not obj.get('takeable', True):
                    return False

                # Use primary name for inventory
                item_name = obj.get('name', object_name)
                self.inventory.append(item_name)
                objects.remove(obj)
                self.score += obj.get('points', 0)
                return True

        return False

    def remove_from_inventory(self, object_name: str) -> Optional[Dict]:
        """Remove object from inventory and return its data."""
        for i, obj in enumerate(self.inventory):
            if self._normalize(obj) == self._normalize(object_name):
                removed = self.inventory.pop(i)
                # Get full object definition
                return self._get_object_definition(removed)

        return None

    def drop_in_room(self, object_name: str) -> bool:
        """Drop an object from inventory into current room."""
        obj_data = self.remove_from_inventory(object_name)
        if obj_data:
            room = self.get_current_room()
            if 'objects' not in room:
                room['objects'] = []
            room['objects'].append(obj_data)
            return True
        return False

    def remove_object_from_room(self, object_name: str) -> bool:
        """Permanently remove an object from the current room."""
        room = self.get_current_room()
        objects = room.get('objects', [])

        for obj in objects:
            if self._matches_object(obj, object_name):
                objects.remove(obj)
                return True

        return False

    def add_object_to_room(self, object_data: Dict, room_id: Optional[str] = None) -> bool:
        """Add an object to a room (current room by default)."""
        if room_id is None:
            room = self.get_current_room()
        else:
            room = self.get_room_by_id(room_id)

        if not room:
            return False

        if 'objects' not in room:
            room['objects'] = []

        room['objects'].append(object_data)
        return True

    def set_flag(self, flag_name: str, value=True):
        """Set a game flag (for tracking events)."""
        self.flags[flag_name] = value

    def get_flag(self, flag_name: str, default=False):
        """Get a game flag value."""
        return self.flags.get(flag_name, default)

    def unlock_exit(self, direction: str, room_id: Optional[str] = None):
        """Unlock an exit in a room."""
        if room_id is None:
            room = self.get_current_room()
        else:
            room = self.get_room_by_id(room_id)

        if not room:
            return False

        exits = room.get('exits', {})
        if direction in exits:
            if isinstance(exits[direction], dict):
                exits[direction]['locked'] = False
                return True

        return False

    def _matches_object(self, obj: Dict, query: str) -> bool:
        """Check if an object matches a query string."""
        query_norm = self._normalize(query)

        # Check primary name
        if self._normalize(obj.get('name', '')) == query_norm:
            return True

        # Check aliases
        for alias in obj.get('aliases', []):
            if self._normalize(alias) == query_norm:
                return True

        return False

    def _normalize(self, text: str) -> str:
        """Normalize text for comparison."""
        return text.lower().strip()

    def get_room_description(self, include_objects: bool = True) -> str:
        """Get a full description of the current room."""
        room = self.get_current_room()

        # Room name and main description
        description = f"\n{room['name']}\n{'=' * len(room['name'])}\n"
        description += room['description']

        # Show objects (if any and if requested)
        if include_objects:
            objects = room.get('objects', [])
            visible_objects = [obj for obj in objects if obj.get('visible', True)]

            if visible_objects:
                description += "\n\n"
                for obj in visible_objects:
                    desc = obj.get('room_description', f"There is a {obj['name']} here.")
                    description += desc + "\n"

        # Show exits
        exits = room.get('exits', {})
        if exits:
            exit_list = []
            for direction, destination in exits.items():
                # Skip locked exits in the list (player can still try them)
                if isinstance(destination, dict):
                    if not destination.get('hidden', False):
                        exit_list.append(direction)
                else:
                    exit_list.append(direction)

            if exit_list:
                description += f"\nExits: {', '.join(sorted(exit_list))}"

        return description

    def save_to_dict(self) -> Dict:
        """Save game state to a dictionary for serialization."""
        return {
            'current_room_id': self.current_room_id,
            'inventory': self.inventory,
            'flags': self.flags,
            'turns': self.turns,
            'score': self.score,
            'visited_rooms': list(self.visited_rooms),
            'world': self.world  # Include modified world state
        }

    @classmethod
    def load_from_dict(cls, data: Dict):
        """Load game state from a dictionary."""
        state = cls(data['world'])
        state.current_room_id = data['current_room_id']
        state.inventory = data['inventory']
        state.flags = data['flags']
        state.turns = data['turns']
        state.score = data.get('score', 0)
        state.visited_rooms = set(data.get('visited_rooms', []))
        return state
