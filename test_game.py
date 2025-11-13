#!/usr/bin/env python3
"""
Test script to validate the game works correctly.
Tests key functionality without requiring user input.
"""

from game_engine import GameEngine
from parser import Parser
from game_state import GameState
from world import get_world_data


def test_parser():
    """Test the parser with various inputs."""
    print("Testing Parser...")
    parser = Parser()

    test_cases = [
        ("take knife", "take", "knife", None),
        ("pick up the knife", "take", "knife", None),
        ("go north", "north", None, None),
        ("n", "north", None, None),
        ("examine painting", "look", "painting", None),
        ("use key on door", "use", "key", "door"),
        ("read journal", "read", "journal", None),
        ("inventory", "inventory", None, None),
        ("i", "inventory", None, None),
    ]

    for input_text, expected_action, expected_target, expected_secondary in test_cases:
        result = parser.parse(input_text)
        assert result['action'] == expected_action, f"Failed: {input_text} -> expected {expected_action}, got {result['action']}"
        assert result['target'] == expected_target, f"Failed target: {input_text}"
        assert result['secondary'] == expected_secondary, f"Failed secondary: {input_text}"
        print(f"  ✓ '{input_text}' -> action:{result['action']}, target:{result['target']}")

    print("Parser tests passed!\n")


def test_game_state():
    """Test game state management."""
    print("Testing Game State...")
    world = get_world_data()
    state = GameState(world)

    # Test initial state
    assert state.current_room_id == 'bedroom'
    print("  ✓ Starts in bedroom")

    # Test inventory
    assert len(state.inventory) == 0
    print("  ✓ Inventory starts empty")

    # Test object detection
    assert state.is_in_current_room('journal')
    print("  ✓ Can detect journal in bedroom")

    # Test taking item
    assert state.add_to_inventory('journal')
    assert state.is_in_inventory('journal')
    print("  ✓ Can take journal")

    # Test movement
    assert state.move_to_room('hallway')
    assert state.current_room_id == 'hallway'
    print("  ✓ Can move to hallway")

    print("Game State tests passed!\n")


def test_game_flow():
    """Test a basic game flow."""
    print("Testing Game Flow...")
    engine = GameEngine()

    # Start new game
    engine.new_game()
    print("  ✓ Game started")

    # Test commands
    commands = [
        ("look", "Your Bedroom"),
        ("inventory", "not carrying"),
        ("take journal", "Taken"),
        ("inventory", "journal"),
        ("north", "Hallway"),
        ("west", "Kitchen"),
        ("take knife", "Taken"),
        ("east", "Hallway"),
        ("south", "Bedroom"),
    ]

    for command, expected_substring in commands:
        result = engine.process_command(command)
        assert result is not None, f"Command '{command}' returned None unexpectedly"
        assert expected_substring.lower() in result.lower(), f"Command '{command}' didn't return expected text. Got: {result[:100]}"
        print(f"  ✓ '{command}' -> contains '{expected_substring}'")

    print("Game Flow tests passed!\n")


def test_puzzle_mechanics():
    """Test puzzle solving."""
    print("Testing Puzzle Mechanics...")
    engine = GameEngine()
    engine.new_game()

    # Get to the garden and pick up stone
    engine.process_command("north")  # to hallway
    engine.process_command("north")  # to garden
    result = engine.process_command("take stone")
    assert "taken" in result.lower()
    print("  ✓ Can take stone")

    # Go to mansion gate
    engine.process_command("north")  # forest path
    result = engine.process_command("north")  # mansion gate
    assert "gate" in result.lower()
    print("  ✓ Reached mansion gate")

    # Try to go through locked gate
    result = engine.process_command("north")
    assert "locked" in result.lower()
    print("  ✓ Gate is locked")

    # Use stone on padlock
    result = engine.process_command("use stone on padlock")
    assert "break" in result.lower() or "open" in result.lower() or "smash" in result.lower()
    print("  ✓ Can break padlock with stone")

    # Now should be able to enter
    result = engine.process_command("north")
    assert "entrance" in result.lower() or "hall" in result.lower()
    print("  ✓ Can enter mansion after breaking lock")

    print("Puzzle Mechanics tests passed!\n")


def test_invalid_commands():
    """Test that invalid commands are properly rejected."""
    print("Testing Invalid Commands...")
    engine = GameEngine()
    engine.new_game()

    # Try to take non-existent object
    result = engine.process_command("take unicorn")
    assert "don't see" in result.lower()
    print("  ✓ Can't take non-existent objects")

    # Try to go in invalid direction
    result = engine.process_command("east")  # no east exit from bedroom
    assert "can't go" in result.lower()
    print("  ✓ Can't go in invalid directions")

    # Try to use object not in inventory
    result = engine.process_command("use magical wand")
    assert "don't" in result.lower()
    print("  ✓ Can't use non-existent objects")

    print("Invalid Commands tests passed!\n")


def main():
    """Run all tests."""
    print("=" * 60)
    print("TESTING THE FORGOTTEN MANSION")
    print("=" * 60)
    print()

    try:
        test_parser()
        test_game_state()
        test_game_flow()
        test_puzzle_mechanics()
        test_invalid_commands()

        print("=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60)
        print("\nThe game is working correctly!")
        print("Run 'python main.py' to play the game.")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
