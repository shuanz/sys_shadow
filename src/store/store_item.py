"""Store item module."""

from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class StoreItem:
    """Represents an item in the store."""
    id: str
    name: str
    description: str
    price: int
    type: str  # tool, upgrade, consumable
    effects: Dict[str, float]  # Skill bonuses or effects
    requirements: Dict[str, int]  # Required skills to use
    level_requirement: int = 1
    stock: int = 1
    is_equipped: bool = False
    
    def can_use(self, player_skills: Dict[str, int], player_level: int) -> bool:
        """Check if the player can use this item.
        
        Args:
            player_skills: Player's skill levels
            player_level: Player's level
            
        Returns:
            bool: True if player can use the item
        """
        if player_level < self.level_requirement:
            return False
            
        for skill, level in self.requirements.items():
            if player_skills.get(skill, 0) < level:
                return False
                
        return True
    
    def apply_effects(self, player_skills: Dict[str, int]) -> Dict[str, float]:
        """Apply item effects to player skills.
        
        Args:
            player_skills: Player's current skill levels
            
        Returns:
            Dict[str, float]: Modified skill levels
        """
        modified_skills = player_skills.copy()
        for skill, bonus in self.effects.items():
            if skill in modified_skills:
                modified_skills[skill] += bonus
        return modified_skills
    
    def to_dict(self) -> Dict:
        """Convert item to dictionary.
        
        Returns:
            Dict: Item data
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "type": self.type,
            "effects": self.effects,
            "requirements": self.requirements,
            "level_requirement": self.level_requirement,
            "stock": self.stock,
            "is_equipped": self.is_equipped
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'StoreItem':
        """Create item from dictionary.
        
        Args:
            data: Item data
            
        Returns:
            StoreItem: Created item
        """
        return cls(**data) 