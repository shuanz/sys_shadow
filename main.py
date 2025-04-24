#!/usr/bin/env python3
"""
Terminal Hacker RPG - Main Game File
"""

import os
from src.ui.terminal import TerminalUI
from src.core.game_state import GameState
from src.core.file_system import FileSystem

def main():
    """Main game loop."""
    ui = TerminalUI()
    game_state = GameState()
    file_system = FileSystem()
    
    # Display welcome screen
    ui.display_welcome()
    
    # Initialize new game
    player_name = ui.display_prompt().strip()
    if not player_name:
        player_name = "h4ck3r"
    game_state.initialize_new_game(player_name)
    
    while not game_state.is_game_over:
        # Display status bar
        player_status = game_state.get_player_status()
        ui.display_status_bar(player_status)
        
        # Get command from user
        command = ui.display_prompt()
        
        if command.lower() == "exit":
            ui.display_info("Logging out...")
            break
        elif command.lower() == "help":
            ui.display_help()
        elif command.lower() == "ls":
            files = file_system.list_directory()
            ui.display_file_list(files)
        elif command.lower().startswith("cd "):
            path = command[3:].strip()
            if file_system.change_directory(path):
                ui.display_success(f"Changed directory to {file_system.get_current_path()}")
            else:
                ui.display_error(f"Directory not found: {path}")
        elif command.lower().startswith("cat "):
            path = command[4:].strip()
            content = file_system.read_file(path)
            if content is not None:
                ui.display_file_content(content)
            else:
                ui.display_error(f"File not found: {path}")
        elif command.lower() == "bank":
            ui.display_info(f"Current balance: {player_status['credits']} credits")
        else:
            ui.display_error(f"Command not recognized: {command}")
        
        # Advance game time
        game_state.advance_time()

if __name__ == "__main__":
    main() 