"""Player class for managing player state and attributes."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import json
import os

@dataclass
class Player:
    """Player class representing the hacker character."""
    
    name: str
    level: int = 1
    credits: int = 100
    experience: int = 0
    inventory: List[str] = field(default_factory=list)
    skills: Dict[str, int] = field(default_factory=dict)
    current_location: str = "home"
    trace_level: int = 0
    
    def __post_init__(self):
        """Initialize default skills if not provided."""
        if not self.skills:
            self.skills = {
                "hacking": 1,
                "stealth": 1,
                "programming": 1,
                "networking": 1
            }
    
    def add_experience(self, amount: int) -> bool:
        """Add experience points and check for level up.
        
        Args:
            amount: Experience points to add
            
        Returns:
            bool: True if player leveled up, False otherwise
        """
        self.experience += amount
        new_level = (self.experience // 100) + 1
        
        if new_level > self.level:
            self.level = new_level
            return True
        return False
    
    def add_credits(self, amount: int) -> None:
        """Add credits to player's balance.
        
        Args:
            amount: Credits to add (can be negative)
        """
        self.credits += amount
        if self.credits < 0:
            self.credits = 0
    
    def add_to_inventory(self, item: str) -> None:
        """Add an item to player's inventory.
        
        Args:
            item: Item to add
        """
        if item not in self.inventory:
            self.inventory.append(item)
    
    def remove_from_inventory(self, item: str) -> bool:
        """Remove an item from player's inventory.
        
        Args:
            item: Item to remove
            
        Returns:
            bool: True if item was removed, False if not found
        """
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def improve_skill(self, skill: str, amount: int = 1) -> None:
        """Improve a skill level.
        
        Args:
            skill: Skill to improve
            amount: Amount to improve by
        """
        if skill in self.skills:
            self.skills[skill] += amount
    
    def get_skill_level(self, skill: str) -> int:
        """Get the level of a specific skill.
        
        Args:
            skill: Skill to check
            
        Returns:
            int: Skill level
        """
        return self.skills.get(skill, 0)
    
    def increase_trace(self, amount: int) -> None:
        """Increase the trace level.
        
        Args:
            amount: Amount to increase by
        """
        self.trace_level += amount
        if self.trace_level > 100:
            self.trace_level = 100
    
    def decrease_trace(self, amount: int) -> None:
        """Decrease the trace level.
        
        Args:
            amount: Amount to decrease by
        """
        self.trace_level -= amount
        if self.trace_level < 0:
            self.trace_level = 0
    
    def save(self, filename: str = "player_save.json") -> None:
        """Save player state to a file.
        
        Args:
            filename: Name of the save file
        """
        save_data = {
            "name": self.name,
            "level": self.level,
            "credits": self.credits,
            "experience": self.experience,
            "inventory": self.inventory,
            "skills": self.skills,
            "current_location": self.current_location,
            "trace_level": self.trace_level
        }
        
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=4)
    
    @classmethod
    def load(cls, filename: str = "player_save.json") -> Optional['Player']:
        """Load player state from a file.
        
        Args:
            filename: Name of the save file
            
        Returns:
            Optional[Player]: Loaded player or None if file doesn't exist
        """
        if not os.path.exists(filename):
            return None
            
        with open(filename, 'r') as f:
            save_data = json.load(f)
            
        return cls(**save_data) 