"""
Game logic - handles all player actions and game mechanics.
"""

from typing import Dict, Tuple
import random


class GameLogic:
    """Processes commands and executes game actions."""

    def __init__(self, game_state):
        self.state = game_state

    def execute_command(self, parsed_command: Dict) -> str:
        """Execute a parsed command and return the result message."""
        action = parsed_command['action']
        target = parsed_command['target']
        secondary = parsed_command['secondary']

        # Route to appropriate handler
        handlers = {
            # Movement
            'north': lambda: self.move('north'),
            'south': lambda: self.move('south'),
            'east': lambda: self.move('east'),
            'west': lambda: self.move('west'),
            'up': lambda: self.move('up'),
            'down': lambda: self.move('down'),

            # Observation
            'look': lambda: self.look(target),
            'read': lambda: self.read(target),
            'search': lambda: self.search(target),
            'listen': lambda: self.listen(),
            'smell': lambda: self.smell(),

            # Manipulation
            'take': lambda: self.take(target),
            'drop': lambda: self.drop(target),
            'use': lambda: self.use(target, secondary),
            'open': lambda: self.open_object(target),
            'close': lambda: self.close_object(target),
            'push': lambda: self.push(target),
            'pull': lambda: self.pull(target),
            'turn': lambda: self.turn(target),
            'eat': lambda: self.eat(target),
            'drink': lambda: self.drink(target),

            # Inventory
            'inventory': lambda: self.show_inventory(),

            # Meta
            'wait': lambda: self.wait(),

            # Unknown
            'unknown': lambda: f"I don't understand '{parsed_command['raw']}'.",
        }

        handler = handlers.get(action)
        if handler:
            return handler()

        return f"You can't {action} that."

    # ===== MOVEMENT =====
    def move(self, direction: str) -> str:
        """Move the player in a direction."""
        room = self.state.get_current_room()
        exits = room.get('exits', {})

        if direction not in exits:
            return f"You can't go {direction} from here."

        exit_info = exits[direction]

        # Handle locked exits
        if isinstance(exit_info, dict):
            destination = exit_info['destination']
            if exit_info.get('locked', False):
                return exit_info.get('locked_message', f"The way {direction} is locked.")
        else:
            destination = exit_info

        # Move to new room
        self.state.move_to_room(destination)
        return self.state.get_room_description()

    # ===== OBSERVATION =====
    def look(self, target: str = None) -> str:
        """Look at the room or an object."""
        if not target:
            return self.state.get_room_description()

        # Look at specific object
        obj = self.state.get_object_anywhere(target)
        if obj:
            return obj.get('description', f"It's just a {target}.")

        return f"You don't see any '{target}' here."

    def read(self, target: str) -> str:
        """Read an object."""
        if not target:
            return "What do you want to read?"

        obj = self.state.get_object_anywhere(target)
        if not obj:
            return f"You don't see any '{target}' here."

        # Check for read interaction
        interactions = obj.get('interactions', {})
        if 'read' in interactions:
            return interactions['read']

        return f"There's nothing to read on the {target}."

    def search(self, target: str) -> str:
        """Search an object or location."""
        if not target:
            return "What do you want to search?"

        obj = self.state.get_object_anywhere(target)
        if not obj:
            return f"You don't see any '{target}' here."

        # Check for search interaction
        interactions = obj.get('interactions', {})
        if 'search' in interactions:
            # Handle special cases where searching reveals items
            result = interactions['search']

            # Check if search reveals a key in the desk
            if 'silver key' in result.lower() and target == 'desk':
                if not self.state.get_flag('desk_searched'):
                    self.state.set_flag('desk_searched', True)
                    # Add silver key to room
                    self.state.add_object_to_room({
                        'name': 'silver key',
                        'aliases': ['key', 'small key'],
                        'description': 'A small silver key. It looks like it fits a door lock.',
                        'takeable': True,
                        'visible': True,
                        'room_description': 'A silver key lies here.',
                        'interactions': {}
                    })
                else:
                    return "You already searched the desk thoroughly."

            # Check if search reveals brass key in wardrobe
            if 'brass key' in result.lower() and target in ['wardrobe', 'closet']:
                if not self.state.get_flag('wardrobe_searched'):
                    self.state.set_flag('wardrobe_searched', True)
                    # Add brass key to room
                    self.state.add_object_to_room({
                        'name': 'brass key',
                        'aliases': ['key', 'small key'],
                        'description': 'A small brass key with ornate engravings.',
                        'takeable': True,
                        'visible': True,
                        'room_description': 'A brass key lies here.',
                        'interactions': {}
                    })
                else:
                    return "You already searched the wardrobe thoroughly."

            # Check if search reveals combination in study desk
            if 'combination' in result.lower() and target in ['study desk', 'desk']:
                if not self.state.get_flag('study_desk_searched'):
                    self.state.set_flag('study_desk_searched', True)
                else:
                    return "You already know the combination: 1847"

            return result

        return f"You search the {target} but find nothing interesting."

    def listen(self) -> str:
        """Listen to surroundings."""
        room_id = self.state.current_room_id
        responses = {
            'forest_path': 'You hear birds chirping and leaves rustling in the wind.',
            'mansion_entrance': 'The mansion is eerily quiet. You hear only the settling of old wood.',
            'garden': 'You hear birds singing and the gentle rustle of the wind through the flowers.',
        }
        return responses.get(room_id, 'You hear nothing unusual.')

    def smell(self) -> str:
        """Smell surroundings."""
        room_id = self.state.current_room_id
        responses = {
            'kitchen': 'You smell stale coffee and old food.',
            'library': 'The smell of old leather and paper fills your nose.',
            'garden': 'The scent of flowers fills the air.',
            'mansion_entrance': 'The air smells of dust and decay.',
        }
        return responses.get(room_id, 'You smell nothing unusual.')

    # ===== MANIPULATION =====
    def take(self, target: str) -> str:
        """Take an object."""
        if not target:
            return "What do you want to take?"

        obj = self.state.get_object_from_room(target)
        if not obj:
            if self.state.is_in_inventory(target):
                return "You already have that."
            return f"You don't see any '{target}' here."

        if not obj.get('takeable', True):
            return f"You can't take the {target}."

        # Add to inventory
        if self.state.add_to_inventory(target):
            item_name = obj.get('name', target)
            return f"Taken: {item_name}"

        return f"You can't take the {target}."

    def drop(self, target: str) -> str:
        """Drop an object from inventory."""
        if not target:
            return "What do you want to drop?"

        if not self.state.is_in_inventory(target):
            return f"You don't have any '{target}'."

        if self.state.drop_in_room(target):
            return f"Dropped: {target}"

        return f"You can't drop the {target}."

    def use(self, target: str, secondary: str = None) -> str:
        """Use an object, optionally on another object."""
        if not target:
            return "What do you want to use?"

        # Check if object exists (in room or inventory)
        in_inventory = self.state.is_in_inventory(target)
        in_room = self.state.is_in_current_room(target)

        if not in_inventory and not in_room:
            return f"You don't have any '{target}'."

        # Special case: using keys
        if 'key' in target.lower():
            return self._use_key(target, secondary)

        # Special case: using knife
        if target == 'knife' and secondary == 'padlock':
            return "The knife isn't strong enough to cut through the padlock."

        # Special case: using stone on padlock
        if target == 'stone' and secondary == 'padlock':
            if self.state.current_room_id == 'mansion_gate':
                if self.state.is_in_inventory('stone'):
                    self.state.unlock_exit('north')
                    self.state.set_flag('gate_unlocked', True)
                    return "You smash the rusty padlock with the stone! It breaks apart and the chain falls away. The gate swings open."
                return "You need to be holding the stone to use it."
            return "There's no padlock here."

        # Get full object data for interaction checks
        obj = self.state.get_object_anywhere(target)
        if obj:
            # Check object-specific use interactions
            interactions = obj.get('interactions', {})
            if 'use' in interactions:
                return interactions['use']

        return f"You can't use the {target} that way."

    def _use_key(self, key_name: str, target: str = None) -> str:
        """Handle using keys on locks."""
        if not self.state.is_in_inventory(key_name):
            return f"You don't have the {key_name}."

        current_room = self.state.current_room_id

        # Silver key opens study door
        if 'silver' in key_name.lower():
            if current_room == 'upstairs_hallway':
                if not target or target == 'door' or target == 'study door':
                    self.state.unlock_exit('east')
                    self.state.set_flag('study_unlocked', True)
                    return "You unlock the study door with the silver key. It swings open with a creak."
                return f"The silver key doesn't fit the {target}."
            return "There's nothing to unlock here with this key."

        # Brass key opens the safe (if player knows combination)
        if 'brass' in key_name.lower():
            if current_room == 'study':
                if target == 'safe':
                    if self.state.get_flag('study_desk_searched'):
                        if not self.state.get_flag('safe_opened'):
                            self.state.set_flag('safe_opened', True)
                            # Add treasure to room
                            self.state.add_object_to_room({
                                'name': 'golden amulet',
                                'aliases': ['amulet', 'gold amulet', 'treasure'],
                                'description': 'A beautiful golden amulet encrusted with gems. This must be the treasure!',
                                'takeable': True,
                                'visible': True,
                                'room_description': 'A golden amulet gleams inside the open safe!',
                                'interactions': {},
                                'points': 100
                            })
                            self.state.score += 50  # Bonus for opening safe
                            return "You insert the brass key and turn it while entering the combination 1847. The safe opens with a satisfying click! Inside, you see a golden amulet!"
                        return "The safe is already open."
                    return "You need to know the combination before you can open the safe with the key."
            return "There's nothing to unlock here with this key."

        return "You're not sure what to use this key on."

    def open_object(self, target: str) -> str:
        """Open something."""
        if not target:
            return "What do you want to open?"

        obj = self.state.get_object_anywhere(target)
        if not obj:
            # Check if trying to open a door
            if 'door' in target.lower():
                room = self.state.get_current_room()
                exits = room.get('exits', {})
                for direction, exit_info in exits.items():
                    if isinstance(exit_info, dict) and exit_info.get('locked'):
                        return exit_info.get('locked_message', 'The door is locked.')
                return "The door is already open."
            return f"You don't see any '{target}' here."

        interactions = obj.get('interactions', {})
        if 'open' in interactions:
            return interactions['open']

        return f"You can't open the {target}."

    def close_object(self, target: str) -> str:
        """Close something."""
        if not target:
            return "What do you want to close?"

        obj = self.state.get_object_anywhere(target)
        if not obj:
            return f"You don't see any '{target}' here."

        interactions = obj.get('interactions', {})
        if 'close' in interactions:
            return interactions['close']

        return f"The {target} is already closed."

    def push(self, target: str) -> str:
        """Push something."""
        if not target:
            return "What do you want to push?"

        obj = self.state.get_object_anywhere(target)
        if not obj:
            return f"You don't see any '{target}' here."

        interactions = obj.get('interactions', {})
        if 'push' in interactions:
            return interactions['push']

        return f"Pushing the {target} doesn't do anything."

    def pull(self, target: str) -> str:
        """Pull something."""
        if not target:
            return "What do you want to pull?"

        obj = self.state.get_object_anywhere(target)
        if not obj:
            return f"You don't see any '{target}' here."

        interactions = obj.get('interactions', {})
        if 'pull' in interactions:
            return interactions['pull']

        return f"Pulling the {target} doesn't do anything."

    def turn(self, target: str) -> str:
        """Turn something."""
        if not target:
            return "What do you want to turn?"

        obj = self.state.get_object_anywhere(target)
        if not obj:
            return f"You don't see any '{target}' here."

        interactions = obj.get('interactions', {})
        if 'turn' in interactions:
            return interactions['turn']

        return f"You can't turn the {target}."

    def eat(self, target: str) -> str:
        """Eat something."""
        if not target:
            return "What do you want to eat?"

        obj = self.state.get_object_anywhere(target)
        if not obj:
            return f"You don't have any '{target}'."

        interactions = obj.get('interactions', {})
        if 'eat' in interactions:
            # Remove from inventory if consumed
            if self.state.is_in_inventory(target):
                self.state.remove_from_inventory(target)
            elif self.state.is_in_current_room(target):
                self.state.remove_object_from_room(target)
            return interactions['eat']

        return f"You can't eat the {target}."

    def drink(self, target: str) -> str:
        """Drink something."""
        if not target:
            return "What do you want to drink?"

        obj = self.state.get_object_anywhere(target)
        if not obj:
            return f"You don't have any '{target}'."

        interactions = obj.get('interactions', {})
        if 'drink' in interactions:
            # Remove from inventory if consumed
            if self.state.is_in_inventory(target):
                self.state.remove_from_inventory(target)
            return interactions['drink']

        return f"You can't drink the {target}."

    # ===== INVENTORY =====
    def show_inventory(self) -> str:
        """Show player's inventory."""
        if not self.state.inventory:
            return "You're not carrying anything."

        items = ", ".join(self.state.inventory)
        return f"You are carrying:\n{items}"

    # ===== META =====
    def wait(self) -> str:
        """Wait/pass time."""
        self.state.turns += 1
        responses = [
            "Time passes...",
            "You wait for a moment.",
            "Nothing happens.",
        ]
        return random.choice(responses)
