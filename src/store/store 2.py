"""Store module."""

from typing import Dict, List, Optional
from .store_item import StoreItem
import json
import os
import random

class Store:
    """Manages the in-game store and its items."""
    
    def __init__(self):
        """Initialize the store."""
        self.items: List[StoreItem] = []
        self._initialize_items()
    
    def _initialize_items(self) -> None:
        """Initialize store items."""
        # Hacking Tools
        self.items.extend([
            StoreItem(
                id="port_scanner",
                name="Port Scanner",
                description="Advanced port scanning tool with stealth capabilities",
                price=1000,
                type="tool",
                effects={"hacking": 0.5, "stealth": 0.2},
                requirements={"hacking": 1},
                level_requirement=1
            ),
            StoreItem(
                id="password_cracker",
                name="Password Cracker",
                description="Brute force password cracking tool",
                price=2000,
                type="tool",
                effects={"hacking": 0.8},
                requirements={"hacking": 2, "programming": 1},
                level_requirement=2
            ),
            StoreItem(
                id="network_analyzer",
                name="Network Analyzer",
                description="Advanced network traffic analysis tool",
                price=3000,
                type="tool",
                effects={"networking": 0.7, "hacking": 0.3},
                requirements={"networking": 2, "hacking": 1},
                level_requirement=3
            )
        ])
        
        # Stealth Tools
        self.items.extend([
            StoreItem(
                id="trace_cleaner",
                name="Trace Cleaner",
                description="Tool to remove traces of your activities",
                price=1500,
                type="tool",
                effects={"stealth": 0.6},
                requirements={"stealth": 1},
                level_requirement=1
            ),
            StoreItem(
                id="proxy_router",
                name="Proxy Router",
                description="Advanced proxy routing system",
                price=2500,
                type="tool",
                effects={"stealth": 0.8, "networking": 0.3},
                requirements={"stealth": 2, "networking": 1},
                level_requirement=2
            )
        ])
        
        # Programming Tools
        self.items.extend([
            StoreItem(
                id="code_analyzer",
                name="Code Analyzer",
                description="Tool to analyze and find vulnerabilities in code",
                price=2000,
                type="tool",
                effects={"programming": 0.6, "hacking": 0.2},
                requirements={"programming": 1},
                level_requirement=1
            ),
            StoreItem(
                id="exploit_generator",
                name="Exploit Generator",
                description="Automated exploit generation tool",
                price=4000,
                type="tool",
                effects={"programming": 0.9, "hacking": 0.4},
                requirements={"programming": 3, "hacking": 2},
                level_requirement=4
            )
        ])
        
        # Consumables
        self.items.extend([
            StoreItem(
                id="trace_reducer",
                name="Trace Reducer",
                description="Temporarily reduces trace level",
                price=500,
                type="consumable",
                effects={"stealth": 0.3},
                requirements={},
                level_requirement=1,
                stock=5
            ),
            StoreItem(
                id="skill_boost",
                name="Skill Boost",
                description="Temporarily increases all skills",
                price=1000,
                type="consumable",
                effects={"hacking": 0.5, "stealth": 0.5, "programming": 0.5, "networking": 0.5},
                requirements={},
                level_requirement=2,
                stock=3
            )
        ])
    
    def get_available_items(self, player_skills: Dict[str, int], player_level: int) -> List[Dict]:
        """Get list of items available to the player.
        
        Args:
            player_skills: Player's skill levels
            player_level: Player's level
            
        Returns:
            List[Dict]: List of available items
        """
        available_items = []
        for item in self.items:
            if item.can_use(player_skills, player_level) and item.stock > 0:
                available_items.append(item.to_dict())
        return available_items
    
    def buy_item(self, item_id: str, player_credits: int) -> Optional[StoreItem]:
        """Buy an item from the store.
        
        Args:
            item_id: ID of the item to buy
            player_credits: Player's current credits
            
        Returns:
            Optional[StoreItem]: Bought item or None if purchase failed
        """
        item = next((i for i in self.items if i.id == item_id), None)
        if not item:
            return None
            
        if item.stock <= 0:
            return None
            
        if player_credits < item.price:
            return None
            
        item.stock -= 1
        return item
    
    def sell_item(self, item: StoreItem) -> int:
        """Sell an item back to the store.
        
        Args:
            item: Item to sell
            
        Returns:
            int: Credits received
        """
        # Items sell for 50% of their purchase price
        sell_price = int(item.price * 0.5)
        item.stock += 1
        return sell_price
    
    def refresh_stock(self) -> None:
        """Refresh store stock."""
        for item in self.items:
            if item.type == "consumable":
                item.stock = random.randint(1, 5)
    
    def save_store(self, filename: str = "store.json") -> None:
        """Save store data to a file.
        
        Args:
            filename: Name of the save file
        """
        store_data = {
            "items": [item.to_dict() for item in self.items]
        }
        
        with open(filename, 'w') as f:
            json.dump(store_data, f, indent=4)
    
    def load_store(self, filename: str = "store.json") -> bool:
        """Load store data from a file.
        
        Args:
            filename: Name of the save file
            
        Returns:
            bool: True if store was loaded successfully
        """
        if not os.path.exists(filename):
            return False
            
        try:
            with open(filename, 'r') as f:
                store_data = json.load(f)
                
            self.items = [
                StoreItem.from_dict(item_data)
                for item_data in store_data.get("items", [])
            ]
            
            return True
        except Exception:
            return False 