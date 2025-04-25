"""Bank module for managing cryptocurrency (cybit) transactions."""

from typing import Dict, List, Optional
from .player import Player
import json
import os
from datetime import datetime

class Bank:
    """Manages the in-game cryptocurrency (cybit) system."""
    
    def __init__(self, player: Player):
        """Initialize the bank system.
        
        Args:
            player: The player instance
        """
        self.player = player
        self.transaction_history: List[Dict] = []
        self.cybit_rate = 1.0  # 1 credit = 1 cybit
        self._load_transaction_history()
    
    def get_balance(self) -> Dict:
        """Get the player's current balance in both credits and cybit.
        
        Returns:
            Dict: Balance information
        """
        return {
            "credits": self.player.credits,
            "cybit": self.player.credits * self.cybit_rate,
            "last_updated": datetime.now().isoformat()
        }
    
    def add_reward(self, amount: int, source: str) -> None:
        """Add a reward to the player's account.
        
        Args:
            amount: Amount of credits to add
            source: Source of the reward (e.g., "mission", "training")
        """
        self.player.add_credits(amount)
        self._record_transaction(amount, "reward", source)
    
    def process_mission_reward(self, mission_data: Dict) -> None:
        """Process rewards from a completed mission.
        
        Args:
            mission_data: Mission data containing reward information
        """
        if not mission_data.get("rewards"):
            return
            
        credits = mission_data["rewards"].get("credits", 0)
        if credits > 0:
            self.add_reward(credits, f"mission_{mission_data.get('id', 'unknown')}")
    
    def _record_transaction(self, amount: int, transaction_type: str, source: str) -> None:
        """Record a transaction in the history.
        
        Args:
            amount: Amount of credits
            transaction_type: Type of transaction
            source: Source of the transaction
        """
        transaction = {
            "timestamp": datetime.now().isoformat(),
            "amount": amount,
            "type": transaction_type,
            "source": source,
            "balance_after": self.player.credits
        }
        self.transaction_history.append(transaction)
        self._save_transaction_history()
    
    def get_transaction_history(self, limit: int = 10) -> List[Dict]:
        """Get the recent transaction history.
        
        Args:
            limit: Maximum number of transactions to return
            
        Returns:
            List[Dict]: Recent transactions
        """
        return self.transaction_history[-limit:]
    
    def _save_transaction_history(self) -> None:
        """Save transaction history to a file."""
        save_data = {
            "transactions": self.transaction_history,
            "last_updated": datetime.now().isoformat()
        }
        
        with open("bank_history.json", "w") as f:
            json.dump(save_data, f, indent=4)
    
    def _load_transaction_history(self) -> None:
        """Load transaction history from a file."""
        if not os.path.exists("bank_history.json"):
            return
            
        try:
            with open("bank_history.json", "r") as f:
                save_data = json.load(f)
                self.transaction_history = save_data.get("transactions", [])
        except Exception:
            self.transaction_history = [] 