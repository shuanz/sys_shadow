"""Faction and reputation system module."""

from typing import Dict, List, Optional
from .player import Player
import json
import os
from datetime import datetime
import random

class FactionSystem:
    """Manages the faction and reputation system."""
    
    def __init__(self, player: Player):
        """Initialize the faction system.
        
        Args:
            player: The player instance
        """
        self.player = player
        self.factions: Dict[str, Dict] = {
            "corporate": {
                "name": "Corporate Alliance",
                "description": "A coalition of megacorporations controlling the city",
                "reputation": 0,
                "missions_completed": 0,
                "missions_failed": 0
            },
            "underground": {
                "name": "Underground Network",
                "description": "A network of independent hackers and activists",
                "reputation": 0,
                "missions_completed": 0,
                "missions_failed": 0
            },
            "government": {
                "name": "City Government",
                "description": "The official city administration and law enforcement",
                "reputation": 0,
                "missions_completed": 0,
                "missions_failed": 0
            }
        }
        self.reputation_history: List[Dict] = []
        self._load_faction_data()
    
    def get_faction_status(self, faction_id: str) -> Dict:
        """Get the status of a specific faction.
        
        Args:
            faction_id: ID of the faction
            
        Returns:
            Dict: Faction status information
        """
        if faction_id not in self.factions:
            return {}
            
        faction = self.factions[faction_id]
        return {
            "id": faction_id,
            "name": faction["name"],
            "description": faction["description"],
            "reputation": faction["reputation"],
            "missions_completed": faction["missions_completed"],
            "missions_failed": faction["missions_failed"],
            "status": self._get_reputation_status(faction["reputation"])
        }
    
    def get_all_faction_status(self) -> List[Dict]:
        """Get status of all factions.
        
        Returns:
            List[Dict]: List of faction statuses
        """
        return [
            self.get_faction_status(faction_id)
            for faction_id in self.factions.keys()
        ]
    
    def update_reputation(self, faction_id: str, amount: int, source: str) -> None:
        """Update reputation with a faction.
        
        Args:
            faction_id: ID of the faction
            amount: Amount to change reputation by
            source: Source of the reputation change
        """
        if faction_id not in self.factions:
            return
            
        self.factions[faction_id]["reputation"] += amount
        self._record_reputation_event(faction_id, amount, source)
        self._save_faction_data()
    
    def process_mission_result(self, faction_id: str, success: bool) -> None:
        """Process the result of a mission for a faction.
        
        Args:
            faction_id: ID of the faction
            success: Whether the mission was successful
        """
        if faction_id not in self.factions:
            return
            
        if success:
            self.factions[faction_id]["missions_completed"] += 1
            self.update_reputation(faction_id, 10, "mission_success")
        else:
            self.factions[faction_id]["missions_failed"] += 1
            self.update_reputation(faction_id, -5, "mission_failure")
    
    def _get_reputation_status(self, reputation: int) -> str:
        """Get the status based on reputation level.
        
        Args:
            reputation: Current reputation value
            
        Returns:
            str: Status description
        """
        if reputation >= 100:
            return "Trusted Ally"
        elif reputation >= 50:
            return "Friendly"
        elif reputation >= 0:
            return "Neutral"
        elif reputation >= -50:
            return "Unfriendly"
        else:
            return "Hostile"
    
    def _record_reputation_event(self, faction_id: str, amount: int, source: str) -> None:
        """Record a reputation change event.
        
        Args:
            faction_id: ID of the faction
            amount: Amount of reputation change
            source: Source of the change
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "faction_id": faction_id,
            "amount": amount,
            "source": source,
            "new_reputation": self.factions[faction_id]["reputation"]
        }
        self.reputation_history.append(event)
    
    def get_reputation_history(self, limit: int = 10) -> List[Dict]:
        """Get recent reputation history.
        
        Args:
            limit: Maximum number of events to return
            
        Returns:
            List[Dict]: Recent reputation events
        """
        return self.reputation_history[-limit:]
    
    def _save_faction_data(self) -> None:
        """Save faction data to a file."""
        save_data = {
            "factions": self.factions,
            "reputation_history": self.reputation_history,
            "last_updated": datetime.now().isoformat()
        }
        
        with open("faction_data.json", "w") as f:
            json.dump(save_data, f, indent=4)
    
    def _load_faction_data(self) -> None:
        """Load faction data from a file."""
        if not os.path.exists("faction_data.json"):
            return
            
        try:
            with open("faction_data.json", "r") as f:
                save_data = json.load(f)
                self.factions = save_data.get("factions", self.factions)
                self.reputation_history = save_data.get("reputation_history", [])
        except Exception:
            pass
    
    def get_available_missions(self, faction_id: str) -> List[Dict]:
        """Get available missions for a faction.
        
        Args:
            faction_id: ID of the faction
            
        Returns:
            List[Dict]: List of available missions
        """
        if faction_id not in self.factions:
            return []
            
        reputation = self.factions[faction_id]["reputation"]
        status = self._get_reputation_status(reputation)
        
        # Generate missions based on reputation status
        missions = []
        if status == "Trusted Ally":
            missions.extend(self._generate_high_level_missions(faction_id))
        if status in ["Trusted Ally", "Friendly"]:
            missions.extend(self._generate_medium_level_missions(faction_id))
        missions.extend(self._generate_low_level_missions(faction_id))
        
        return missions
    
    def _generate_low_level_missions(self, faction_id: str) -> List[Dict]:
        """Generate low-level missions for a faction.
        
        Args:
            faction_id: ID of the faction
            
        Returns:
            List[Dict]: List of low-level missions
        """
        return [
            {
                "id": f"mission_{faction_id}_low_{i}",
                "name": f"Basic {self.factions[faction_id]['name']} Mission",
                "difficulty": 1,
                "rewards": {
                    "credits": 100,
                    "experience": 50
                }
            }
            for i in range(3)
        ]
    
    def _generate_medium_level_missions(self, faction_id: str) -> List[Dict]:
        """Generate medium-level missions for a faction.
        
        Args:
            faction_id: ID of the faction
            
        Returns:
            List[Dict]: List of medium-level missions
        """
        return [
            {
                "id": f"mission_{faction_id}_med_{i}",
                "name": f"Advanced {self.factions[faction_id]['name']} Mission",
                "difficulty": 2,
                "rewards": {
                    "credits": 250,
                    "experience": 100
                }
            }
            for i in range(2)
        ]
    
    def _generate_high_level_missions(self, faction_id: str) -> List[Dict]:
        """Generate high-level missions for a faction.
        
        Args:
            faction_id: ID of the faction
            
        Returns:
            List[Dict]: List of high-level missions
        """
        return [
            {
                "id": f"mission_{faction_id}_high_{i}",
                "name": f"Elite {self.factions[faction_id]['name']} Mission",
                "difficulty": 3,
                "rewards": {
                    "credits": 500,
                    "experience": 200
                }
            }
            for i in range(1)
        ] 