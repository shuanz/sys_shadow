"""Mission management module."""

from typing import Dict, List, Optional
from .mission_generator import Mission, MissionGenerator
from src.core.player import Player
from src.core.file_system import FileSystem
import json
import os

class MissionManager:
    """Manages missions and their execution."""
    
    def __init__(self, player: Player, file_system: FileSystem):
        """Initialize the mission manager.
        
        Args:
            player: Player instance
            file_system: FileSystem instance
        """
        self.player = player
        self.file_system = file_system
        self.generator = MissionGenerator()
        self.current_mission: Optional[Mission] = None
        self.available_missions: List[Mission] = []
        self.mission_history: List[Dict] = []
        self.mission_progress: Dict = {}
    
    def refresh_available_missions(self) -> None:
        """Refresh the list of available missions."""
        self.available_missions = self.generator.get_available_missions(
            self.player.level
        )
    
    def start_mission(self, mission_id: str) -> bool:
        """Start a mission.
        
        Args:
            mission_id: ID of the mission to start
            
        Returns:
            bool: True if mission was started successfully
        """
        # Find the mission
        mission = next(
            (m for m in self.available_missions if m.id == mission_id),
            None
        )
        
        if not mission:
            return False
            
        # Check if player meets requirements
        for skill, level in mission.required_skills.items():
            if self.player.get_skill_level(skill) < level:
                return False
        
        # Start the mission
        self.current_mission = mission
        self.available_missions.remove(mission)
        
        # Initialize mission progress
        self.mission_progress = {
            "started_at": mission.created_at,
            "current_step": 0,
            "completed_steps": [],
            "trace_level": 0
        }
        
        # Generate target system
        self.file_system.generate_target_system(mission.difficulty)
        
        return True
    
    def complete_mission(self, success: bool) -> None:
        """Complete the current mission.
        
        Args:
            success: Whether the mission was successful
        """
        if not self.current_mission:
            return
            
        # Update mission history
        self.mission_history.append({
            "mission_id": self.current_mission.id,
            "name": self.current_mission.name,
            "target": self.current_mission.target,
            "difficulty": self.current_mission.difficulty,
            "success": success,
            "trace_level": self.mission_progress["trace_level"],
            "completed_at": self.current_mission.created_at
        })
        
        # Update player state
        if success:
            self.player.add_experience(self.current_mission.experience_reward)
            self.player.add_credits(self.current_mission.credit_reward)
            
            # Improve skills based on mission type
            for skill in self.current_mission.required_skills:
                self.player.improve_skill(skill)
        
        # Reset mission state
        self.current_mission = None
        self.mission_progress = {}
    
    def update_mission_progress(self, step: int, trace_increase: int = 0) -> None:
        """Update mission progress.
        
        Args:
            step: Current step in the mission
            trace_increase: Amount to increase trace level
        """
        if not self.current_mission:
            return
            
        self.mission_progress["current_step"] = step
        self.mission_progress["trace_level"] += trace_increase
        
        # Check for mission failure
        if self.mission_progress["trace_level"] >= 100:
            self.complete_mission(False)
    
    def get_mission_status(self) -> Dict:
        """Get current mission status.
        
        Returns:
            Dict: Mission status information
        """
        if not self.current_mission:
            return {}
            
        return {
            "id": self.current_mission.id,
            "name": self.current_mission.name,
            "description": self.current_mission.description,
            "target": self.current_mission.target,
            "difficulty": self.current_mission.difficulty,
            "current_step": self.mission_progress["current_step"],
            "trace_level": self.mission_progress["trace_level"],
            "time_limit": self.current_mission.time_limit
        }
    
    def get_available_missions(self) -> List[Dict]:
        """Get list of available missions.
        
        Returns:
            List[Dict]: List of available missions
        """
        return [
            {
                "id": mission.id,
                "name": mission.name,
                "description": mission.description,
                "target": mission.target,
                "difficulty": mission.difficulty,
                "rewards": {
                    "credits": mission.credit_reward,
                    "experience": mission.experience_reward
                },
                "required_skills": mission.required_skills
            }
            for mission in self.available_missions
        ]
    
    def get_mission_history(self) -> List[Dict]:
        """Get mission history.
        
        Returns:
            List[Dict]: Mission history
        """
        return self.mission_history
    
    def save_missions(self, filename: str = "missions.json") -> None:
        """Save mission data to a file.
        
        Args:
            filename: Name of the save file
        """
        save_data = {
            "current_mission": self.current_mission.__dict__ if self.current_mission else None,
            "available_missions": [m.__dict__ for m in self.available_missions],
            "mission_history": self.mission_history,
            "mission_progress": self.mission_progress
        }
        
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=4)
    
    def load_missions(self, filename: str = "missions.json") -> bool:
        """Load mission data from a file.
        
        Args:
            filename: Name of the save file
            
        Returns:
            bool: True if missions were loaded successfully
        """
        if not os.path.exists(filename):
            return False
            
        try:
            with open(filename, 'r') as f:
                save_data = json.load(f)
                
            # Load current mission
            if save_data.get("current_mission"):
                self.current_mission = Mission(**save_data["current_mission"])
            
            # Load available missions
            self.available_missions = [
                Mission(**mission_data)
                for mission_data in save_data.get("available_missions", [])
            ]
            
            # Load mission history and progress
            self.mission_history = save_data.get("mission_history", [])
            self.mission_progress = save_data.get("mission_progress", {})
            
            return True
        except Exception:
            return False 