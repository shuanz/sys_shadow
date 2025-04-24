"""Game state management module."""

from typing import Dict, List, Optional
from .player import Player
import json
import os

class GameState:
    """Class to manage the global game state."""
    
    def __init__(self):
        """Initialize the game state."""
        self.player: Optional[Player] = None
        self.current_mission: Optional[Dict] = None
        self.mission_history: List[Dict] = []
        self.game_time: int = 0
        self.is_game_over: bool = False
        
    def initialize_new_game(self, player_name: str) -> None:
        """Initialize a new game with a new player.
        
        Args:
            player_name: Name of the player
        """
        self.player = Player(name=player_name)
        self.current_mission = None
        self.mission_history = []
        self.game_time = 0
        self.is_game_over = False
    
    def load_game(self, save_file: str = "game_save.json") -> bool:
        """Load a saved game.
        
        Args:
            save_file: Name of the save file
            
        Returns:
            bool: True if game was loaded successfully, False otherwise
        """
        if not os.path.exists(save_file):
            return False
            
        try:
            with open(save_file, 'r') as f:
                save_data = json.load(f)
                
            self.player = Player.load(save_data.get('player_file', 'player_save.json'))
            self.current_mission = save_data.get('current_mission')
            self.mission_history = save_data.get('mission_history', [])
            self.game_time = save_data.get('game_time', 0)
            self.is_game_over = save_data.get('is_game_over', False)
            
            return True
        except Exception:
            return False
    
    def save_game(self, save_file: str = "game_save.json") -> None:
        """Save the current game state.
        
        Args:
            save_file: Name of the save file
        """
        if not self.player:
            return
            
        self.player.save()
        
        save_data = {
            'player_file': 'player_save.json',
            'current_mission': self.current_mission,
            'mission_history': self.mission_history,
            'game_time': self.game_time,
            'is_game_over': self.is_game_over
        }
        
        with open(save_file, 'w') as f:
            json.dump(save_data, f, indent=4)
    
    def start_mission(self, mission_data: Dict) -> None:
        """Start a new mission.
        
        Args:
            mission_data: Mission data dictionary
        """
        self.current_mission = mission_data
        self.mission_history.append({
            'mission_id': mission_data.get('id'),
            'start_time': self.game_time,
            'status': 'in_progress'
        })
    
    def complete_mission(self, success: bool) -> None:
        """Complete the current mission.
        
        Args:
            success: Whether the mission was successful
        """
        if not self.current_mission:
            return
            
        # Update mission history
        for mission in self.mission_history:
            if mission['mission_id'] == self.current_mission.get('id'):
                mission['status'] = 'completed' if success else 'failed'
                mission['end_time'] = self.game_time
                break
        
        # Update player state
        if success and self.player:
            self.player.add_experience(self.current_mission.get('experience_reward', 0))
            self.player.add_credits(self.current_mission.get('credit_reward', 0))
        
        self.current_mission = None
    
    def advance_time(self, amount: int = 1) -> None:
        """Advance the game time.
        
        Args:
            amount: Amount of time to advance
        """
        self.game_time += amount
        
        # Check for game over conditions
        if self.player and self.player.trace_level >= 100:
            self.is_game_over = True
    
    def get_player_status(self) -> Dict:
        """Get the current player status.
        
        Returns:
            Dict: Player status information
        """
        if not self.player:
            return {}
            
        return {
            'name': self.player.name,
            'level': self.player.level,
            'credits': self.player.credits,
            'experience': self.player.experience,
            'skills': self.player.skills,
            'trace_level': self.player.trace_level,
            'current_location': self.player.current_location
        }
    
    def get_mission_status(self) -> Dict:
        """Get the current mission status.
        
        Returns:
            Dict: Mission status information
        """
        if not self.current_mission:
            return {}
            
        return {
            'id': self.current_mission.get('id'),
            'name': self.current_mission.get('name'),
            'description': self.current_mission.get('description'),
            'difficulty': self.current_mission.get('difficulty'),
            'time_elapsed': self.game_time - self.mission_history[-1]['start_time']
        } 