#!/usr/bin/env python3
"""
Terminal Hacker RPG - Main Game File
"""

import os
from src.ui.terminal import TerminalUI
from src.core.game_state import GameState
from src.core.file_system import FileSystem
from src.missions.mission_manager import MissionManager

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
    
    # Initialize mission manager
    mission_manager = MissionManager(game_state.player, file_system)
    mission_manager.refresh_available_missions()
    
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
        elif command.lower() == "missions":
            # Display available missions
            missions = mission_manager.get_available_missions()
            if missions:
                ui.display_info("Available Missions:")
                for mission in missions:
                    ui.display_info(f"\n{mission['name']}")
                    ui.display_info(f"Target: {mission['target']}")
                    ui.display_info(f"Difficulty: {mission['difficulty']}")
                    ui.display_info(f"Rewards: {mission['rewards']['credits']} credits, {mission['rewards']['experience']} XP")
                    ui.display_info(f"Required Skills: {', '.join(f'{k} {v}' for k, v in mission['required_skills'].items())}")
            else:
                ui.display_info("No missions available. Check back later.")
        elif command.lower().startswith("accept "):
            mission_id = command[7:].strip()
            if mission_manager.start_mission(mission_id):
                ui.display_success("Mission accepted!")
                mission_status = mission_manager.get_mission_status()
                ui.display_info(f"\nMission: {mission_status['name']}")
                ui.display_info(f"Target: {mission_status['target']}")
                ui.display_info(f"Description: {mission_status['description']}")
            else:
                ui.display_error("Failed to start mission. Check requirements.")
        elif command.lower() == "status":
            mission_status = mission_manager.get_mission_status()
            if mission_status:
                ui.display_info(f"\nCurrent Mission: {mission_status['name']}")
                ui.display_info(f"Progress: Step {mission_status['current_step']}")
                ui.display_info(f"Trace Level: {mission_status['trace_level']}%")
            else:
                ui.display_info("No active mission.")
        else:
            ui.display_error(f"Command not recognized: {command}")
        
        # Advance game time
        game_state.advance_time()

if __name__ == "__main__":
    main() 