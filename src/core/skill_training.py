"""Skill training and development module."""

from typing import Dict, List, Optional
from .player import Player
import random

class SkillTraining:
    """Class to manage skill training and development."""
    
    def __init__(self, player: Player):
        """Initialize the skill training system.
        
        Args:
            player: The player instance
        """
        self.player = player
        self.training_costs = {
            "hacking": 50,
            "stealth": 40,
            "programming": 45,
            "networking": 35
        }
        
        self.training_experience = {
            "hacking": 20,
            "stealth": 15,
            "programming": 25,
            "networking": 20
        }
    
    def get_available_training(self) -> List[Dict]:
        """Get available training options.
        
        Returns:
            List[Dict]: List of available training options
        """
        return [
            {
                "skill": skill,
                "cost": self.training_costs[skill],
                "experience": self.training_experience[skill],
                "current_level": self.player.get_skill_level(skill)
            }
            for skill in self.player.skills.keys()
        ]
    
    def train_skill(self, skill: str) -> bool:
        """Train a specific skill.
        
        Args:
            skill: Skill to train
            
        Returns:
            bool: True if training was successful, False otherwise
        """
        if skill not in self.player.skills:
            return False
            
        cost = self.training_costs[skill]
        if self.player.credits < cost:
            return False
            
        # Deduct training cost
        self.player.add_credits(-cost)
        
        # Add experience
        self.player.add_experience(self.training_experience[skill])
        
        # Improve skill with random chance based on current level
        current_level = self.player.get_skill_level(skill)
        success_chance = max(0.1, 1.0 - (current_level * 0.1))
        
        if random.random() < success_chance:
            self.player.improve_skill(skill)
            return True
            
        return False
    
    def get_training_progress(self, skill: str) -> Dict:
        """Get training progress for a skill.
        
        Args:
            skill: Skill to check
            
        Returns:
            Dict: Training progress information
        """
        if skill not in self.player.skills:
            return {}
            
        current_level = self.player.get_skill_level(skill)
        next_level_cost = self.training_costs[skill] * (current_level + 1)
        
        return {
            "skill": skill,
            "current_level": current_level,
            "next_level_cost": next_level_cost,
            "success_chance": max(0.1, 1.0 - (current_level * 0.1))
        } 