#!/usr/bin/env python3
"""
GUI launcher for The Forgotten Mansion.
Creates a terminal-like window for playing the game.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, font
import threading
import queue
from game_engine import GameEngine


class TerminalGUI:
    """Terminal-style GUI for the text adventure game."""

    def __init__(self, root):
        self.root = root
        self.root.title("The Forgotten Mansion")
        self.root.geometry("900x700")

        # Create game engine
        self.engine = GameEngine()

        # Queue for thread-safe communication
        self.output_queue = queue.Queue()

        # Configure colors (classic terminal look)
        self.bg_color = "#0C0C0C"  # Dark background
        self.fg_color = "#CCCCCC"  # Light gray text
        self.input_color = "#00FF00"  # Green for input (classic terminal)
        self.prompt_color = "#00AAFF"  # Cyan for prompt

        self.setup_ui()
        self.game_running = False

        # Start the game
        self.start_game()

    def setup_ui(self):
        """Set up the user interface."""
        # Configure root window
        self.root.configure(bg=self.bg_color)

        # Create main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create scrolled text widget for game output
        self.output_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            bg=self.bg_color,
            fg=self.fg_color,
            insertbackground=self.input_color,  # Cursor color
            font=("Courier New", 11),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # Configure text tags for different colors
        self.output_text.tag_config("prompt", foreground=self.prompt_color, font=("Courier New", 11, "bold"))
        self.output_text.tag_config("input", foreground=self.input_color)
        self.output_text.tag_config("output", foreground=self.fg_color)
        self.output_text.tag_config("header", foreground="#FFFF00", font=("Courier New", 11, "bold"))
        self.output_text.tag_config("error", foreground="#FF6666")

        # Create input frame
        input_frame = tk.Frame(main_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=(10, 0))

        # Create prompt label
        self.prompt_label = tk.Label(
            input_frame,
            text="> ",
            bg=self.bg_color,
            fg=self.prompt_color,
            font=("Courier New", 11, "bold")
        )
        self.prompt_label.pack(side=tk.LEFT)

        # Create input entry
        self.input_entry = tk.Entry(
            input_frame,
            bg=self.bg_color,
            fg=self.input_color,
            insertbackground=self.input_color,
            font=("Courier New", 11),
            relief=tk.FLAT,
            borderwidth=2
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_entry.focus()

        # Bind enter key to submit command
        self.input_entry.bind("<Return>", self.submit_command)

        # Bind up/down arrows for command history
        self.input_entry.bind("<Up>", self.previous_command)
        self.input_entry.bind("<Down>", self.next_command)

        # Command history
        self.command_history = []
        self.history_index = -1

        # Create menu bar
        self.create_menu()

        # Make output text read-only
        self.output_text.bind("<Key>", lambda e: "break")  # Disable typing in output

    def create_menu(self):
        """Create the menu bar."""
        menubar = tk.Menu(self.root, bg=self.bg_color, fg=self.fg_color)
        self.root.config(menu=menubar)

        # Game menu
        game_menu = tk.Menu(menubar, tearoff=0, bg=self.bg_color, fg=self.fg_color)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.new_game)
        game_menu.add_command(label="Save Game", command=self.save_game)
        game_menu.add_command(label="Load Game", command=self.load_game)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.quit_game)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0, bg=self.bg_color, fg=self.fg_color)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Increase Font Size", command=lambda: self.change_font_size(1))
        view_menu.add_command(label="Decrease Font Size", command=lambda: self.change_font_size(-1))
        view_menu.add_separator()
        view_menu.add_command(label="Clear Screen", command=self.clear_screen)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.bg_color, fg=self.fg_color)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Commands", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)

    def start_game(self):
        """Start a new game."""
        self.game_running = True
        self.output_text.delete(1.0, tk.END)

        # Start game in a separate thread to avoid blocking UI
        thread = threading.Thread(target=self._game_init_thread, daemon=True)
        thread.start()

    def _game_init_thread(self):
        """Initialize the game in a separate thread."""
        # Capture the intro and initial room description
        import io
        import sys

        # Redirect stdout to capture the intro
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        initial_message = self.engine.new_game()

        # Get the captured intro
        intro = sys.stdout.getvalue()
        sys.stdout = old_stdout

        # Display intro
        self.display_output(intro)
        self.display_output(initial_message + "\n")
        self.display_prompt()

    def new_game(self):
        """Start a new game (menu option)."""
        if messagebox.askyesno("New Game", "Are you sure you want to start a new game? Any unsaved progress will be lost."):
            self.start_game()

    def save_game(self):
        """Save the current game."""
        result = self.engine.save_game()
        self.display_output(f"\n{result}\n")
        self.display_prompt()

    def load_game(self):
        """Load a saved game."""
        result = self.engine.load_game()
        self.output_text.delete(1.0, tk.END)
        self.display_output(result + "\n")
        self.display_prompt()
        self.game_running = True

    def quit_game(self):
        """Quit the game."""
        if self.game_running:
            if messagebox.askyesno("Quit", "Are you sure you want to quit? Don't forget to save your game!"):
                self.root.quit()
        else:
            self.root.quit()

    def submit_command(self, event=None):
        """Process a command when Enter is pressed."""
        command = self.input_entry.get().strip()

        if not command:
            return

        # Add to command history
        if command:
            self.command_history.append(command)
            self.history_index = len(self.command_history)

        # Display the command in output
        self.display_input(command)

        # Clear input
        self.input_entry.delete(0, tk.END)

        # Process command
        self.process_command(command)

    def process_command(self, command):
        """Process a game command."""
        if not self.game_running:
            return

        # Process the command through the game engine
        response = self.engine.process_command(command)

        # Check if game should quit
        if response is None:
            self.display_output("\nThanks for playing!\n")
            self.game_running = False
            if messagebox.askyesno("Game Over", "Thanks for playing! Would you like to exit?"):
                self.root.quit()
            return

        # Display response
        if response:
            self.display_output(f"\n{response}\n")

        # Check if game is still running (might have ended due to win condition)
        if self.engine.running:
            self.display_prompt()
        else:
            self.game_running = False

    def display_output(self, text):
        """Display text in the output area."""
        self.output_text.insert(tk.END, text, "output")
        self.output_text.see(tk.END)

    def display_input(self, text):
        """Display user input in the output area."""
        self.output_text.insert(tk.END, "> ", "prompt")
        self.output_text.insert(tk.END, text + "\n", "input")
        self.output_text.see(tk.END)

    def display_prompt(self):
        """Display the command prompt (done via the input entry)."""
        # The prompt is already shown in the input_frame, no need to add to output
        pass

    def previous_command(self, event=None):
        """Navigate to previous command in history."""
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.command_history[self.history_index])
        return "break"  # Prevent default behavior

    def next_command(self, event=None):
        """Navigate to next command in history."""
        if self.command_history:
            self.history_index += 1
            self.input_entry.delete(0, tk.END)
            if self.history_index < len(self.command_history):
                self.input_entry.insert(0, self.command_history[self.history_index])
            else:
                self.history_index = len(self.command_history)
        return "break"  # Prevent default behavior

    def change_font_size(self, delta):
        """Change the font size."""
        current_font = font.Font(font=self.output_text['font'])
        new_size = current_font.actual()['size'] + delta
        new_size = max(8, min(20, new_size))  # Clamp between 8 and 20

        new_font = ("Courier New", new_size)
        self.output_text.configure(font=new_font)
        self.input_entry.configure(font=new_font)

        # Update tags
        self.output_text.tag_config("prompt", font=(new_font[0], new_font[1], "bold"))
        self.output_text.tag_config("header", font=(new_font[0], new_font[1], "bold"))

    def clear_screen(self):
        """Clear the screen."""
        if messagebox.askyesno("Clear Screen", "Are you sure you want to clear the screen?"):
            self.output_text.delete(1.0, tk.END)
            self.display_prompt()

    def show_help(self):
        """Show help dialog."""
        help_text = self.engine.parser.get_help_text()

        # Create a new window for help
        help_window = tk.Toplevel(self.root)
        help_window.title("Game Commands")
        help_window.geometry("700x600")
        help_window.configure(bg=self.bg_color)

        # Create scrolled text for help
        help_text_widget = scrolledtext.ScrolledText(
            help_window,
            wrap=tk.WORD,
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Courier New", 10),
            padx=10,
            pady=10
        )
        help_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        help_text_widget.insert(1.0, help_text)
        help_text_widget.configure(state=tk.DISABLED)

        # Close button
        close_btn = tk.Button(
            help_window,
            text="Close",
            command=help_window.destroy,
            bg="#333333",
            fg=self.fg_color,
            font=("Courier New", 10)
        )
        close_btn.pack(pady=10)

    def show_about(self):
        """Show about dialog."""
        about_text = """
The Forgotten Mansion
A Text Adventure Game

Version 1.0

A classic-style text adventure with a robust
parser and rich interactive world.

Explore the mansion, solve puzzles, and
discover the legendary treasure!

Built with Python & Tkinter
        """
        messagebox.showinfo("About The Forgotten Mansion", about_text)


def main():
    """Entry point for GUI version."""
    root = tk.Tk()
    app = TerminalGUI(root)

    # Handle window close
    root.protocol("WM_DELETE_WINDOW", app.quit_game)

    # Start the GUI
    root.mainloop()


if __name__ == '__main__':
    main()
