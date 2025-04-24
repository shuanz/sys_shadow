#!/usr/bin/env python3
"""
Terminal Hacker RPG - Main Game File
"""

import os
from src.ui.terminal import TerminalUI
from src.core.game_state import GameState
from src.core.file_system import FileSystem
from src.missions.mission_manager import MissionManager
from src.hacking.interface import HackingInterface
from src.store.interface import StoreInterface
from src.core.skill_training import SkillTraining
from src.core.bank import Bank

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
    
    # Initialize hacking interface
    hacking_interface = HackingInterface(game_state.player, ui)
    
    # Initialize store interface
    store_interface = StoreInterface(game_state.player, ui)
    
    # Initialize skill training
    skill_training = SkillTraining(game_state.player)
    
    # Initialize bank
    bank = Bank(game_state.player)
    
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
            balance = bank.get_balance()
            ui.display_info(f"\nCurrent Balance:")
            ui.display_info(f"Credits: {balance['credits']}")
            ui.display_info(f"Cybit: {balance['cybit']:.2f}")
            ui.display_info(f"Last Updated: {balance['last_updated']}")
            
            # Show recent transactions
            transactions = bank.get_transaction_history(5)
            if transactions:
                ui.display_info("\nRecent Transactions:")
                for tx in transactions:
                    ui.display_info(f"\n{tx['timestamp']}")
                    ui.display_info(f"Type: {tx['type']}")
                    ui.display_info(f"Amount: {tx['amount']} credits")
                    ui.display_info(f"Source: {tx['source']}")
                    ui.display_info(f"Balance: {tx['balance_after']} credits")
        elif command.lower() == "missions":
            # Display available missions
            missions = mission_manager.get_available_missions()
            if missions:
                ui.display_info("Available Missions:")
                for mission in missions:
                    ui.display_info(f"\n{mission['name']}")
                    ui.display_info(f"ID: {mission['id']}")
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
                
                # Start hacking interface
                hacking_interface.start_hacking(mission_status['difficulty'])
                
                # Enter hacking mode
                while True:
                    hack_command = ui.display_prompt()
                    if not hacking_interface.handle_command(hack_command):
                        break
                
                # Complete mission if hacking was successful
                if hacking_interface.simulation and hacking_interface.simulation.is_complete():
                    mission_manager.complete_mission(True)
                    ui.display_success("Mission completed successfully!")
                    # Process mission rewards
                    bank.process_mission_reward(mission_status)
                else:
                    mission_manager.complete_mission(False)
                    ui.display_error("Mission failed!")
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
        elif command.lower() == "store":
            # Enter store mode
            store_interface.start()
        elif command.lower() == "train":
            # Display available training options
            training_options = skill_training.get_available_training()
            ui.display_info("\nAvailable Training:")
            for option in training_options:
                ui.display_info(f"\n{option['skill'].title()}")
                ui.display_info(f"Current Level: {option['current_level']}")
                ui.display_info(f"Cost: {option['cost']} credits")
                ui.display_info(f"Experience: {option['experience']} XP")
        elif command.lower().startswith("train "):
            skill = command[6:].strip().lower()
            if skill_training.train_skill(skill):
                ui.display_success(f"Successfully trained {skill}!")
                progress = skill_training.get_training_progress(skill)
                ui.display_info(f"New level: {progress['current_level']}")
                ui.display_info(f"Next level cost: {progress['next_level_cost']} credits")
                ui.display_info(f"Success chance: {progress['success_chance']*100:.1f}%")
            else:
                ui.display_error(f"Failed to train {skill}. Check your credits and try again.")
        else:
            ui.display_error(f"Command not recognized: {command}")
        
        # Advance game time
        game_state.advance_time()

if __name__ == "__main__":
    main() 