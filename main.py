#!/usr/bin/env python3
"""
Terminal Hacker RPG - Main Game File
"""

import os
from src.ui.terminal import TerminalUI

def main():
    """Main game loop."""
    ui = TerminalUI()
    ui.display_welcome()
    
    # Initial game state
    game_state = {
        "credits": 100,
        "level": 1,
        "trace": 0
    }
    
    while True:
        # Display status bar
        ui.display_status_bar(game_state)
        
        # Get command from user
        command = ui.display_prompt()
        
        if command.lower() == "exit":
            ui.display_info("Logging out...")
            break
        elif command.lower() == "help":
            ui.display_help()
        elif command.lower() == "ls":
            # Example file list
            files = [
                {"name": "readme.txt", "size": "1.2KB", "type": "text"},
                {"name": "config.dat", "size": "4.5KB", "type": "data"},
                {"name": "logs/", "size": "0B", "type": "dir"}
            ]
            ui.display_file_list(files)
        elif command.lower() == "cat readme.txt":
            ui.display_file_content("Welcome to the Terminal Hacker RPG!\n\nThis is a cyberpunk-themed game where you play as a hacker.")
        elif command.lower() == "bank":
            ui.display_info(f"Current balance: {game_state['credits']} credits")
        else:
            ui.display_error(f"Command not recognized: {command}")

if __name__ == "__main__":
    main() 