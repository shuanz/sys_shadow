"""Trace and exposure system module."""

from typing import Dict, List, Optional
from .player import Player
import json
import os
from datetime import datetime
import random

class TraceSystem:
    """Manages the trace and exposure system for player actions."""
    
    def __init__(self, player: Player):
        """Initialize the trace system.
        
        Args:
            player: The player instance
        """
        self.player = player
        self.trace_history: List[Dict] = []
        self.exposure_level: int = 0
        self._load_trace_history()
    
    def increase_trace(self, amount: int, source: str) -> None:
        """Increase the trace level.
        
        Args:
            amount: Amount to increase
            source: Source of the trace increase
        """
        self.player.trace_level += amount
        if self.player.trace_level > 100:
            self.player.trace_level = 100
            
        self._record_trace_event(amount, "increase", source)
        self._check_exposure()
    
    def decrease_trace(self, amount: int, source: str) -> None:
        """Decrease the trace level.
        
        Args:
            amount: Amount to decrease
            source: Source of the trace decrease
        """
        self.player.trace_level -= amount
        if self.player.trace_level < 0:
            self.player.trace_level = 0
            
        self._record_trace_event(-amount, "decrease", source)
    
    def _check_exposure(self) -> None:
        """Check if player has been exposed based on trace level."""
        if self.player.trace_level >= 100:
            self.exposure_level = 100
            self._record_exposure_event()
        elif self.player.trace_level >= 75:
            self.exposure_level = 75
            self._record_exposure_event()
        elif self.player.trace_level >= 50:
            self.exposure_level = 50
            self._record_exposure_event()
    
    def _record_trace_event(self, amount: int, event_type: str, source: str) -> None:
        """Record a trace event.
        
        Args:
            amount: Amount of trace change
            event_type: Type of event
            source: Source of the event
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "amount": amount,
            "type": event_type,
            "source": source,
            "trace_level": self.player.trace_level,
            "exposure_level": self.exposure_level
        }
        self.trace_history.append(event)
        self._save_trace_history()
    
    def _record_exposure_event(self) -> None:
        """Record an exposure event."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": "exposure",
            "trace_level": self.player.trace_level,
            "exposure_level": self.exposure_level
        }
        self.trace_history.append(event)
        self._save_trace_history()
    
    def get_trace_status(self) -> Dict:
        """Get current trace and exposure status.
        
        Returns:
            Dict: Status information
        """
        return {
            "trace_level": self.player.trace_level,
            "exposure_level": self.exposure_level,
            "last_updated": datetime.now().isoformat()
        }
    
    def get_trace_history(self, limit: int = 10) -> List[Dict]:
        """Get recent trace history.
        
        Args:
            limit: Maximum number of events to return
            
        Returns:
            List[Dict]: Recent trace events
        """
        return self.trace_history[-limit:]
    
    def _save_trace_history(self) -> None:
        """Save trace history to a file."""
        save_data = {
            "trace_history": self.trace_history,
            "exposure_level": self.exposure_level,
            "last_updated": datetime.now().isoformat()
        }
        
        with open("trace_history.json", "w") as f:
            json.dump(save_data, f, indent=4)
    
    def _load_trace_history(self) -> None:
        """Load trace history from a file."""
        if not os.path.exists("trace_history.json"):
            return
            
        try:
            with open("trace_history.json", "r") as f:
                save_data = json.load(f)
                self.trace_history = save_data.get("trace_history", [])
                self.exposure_level = save_data.get("exposure_level", 0)
        except Exception:
            self.trace_history = []
            self.exposure_level = 0
    
    def calculate_risk(self, action: str) -> Dict:
        """Calculate risk for a specific action.
        
        Args:
            action: Action to calculate risk for
            
        Returns:
            Dict: Risk information
        """
        base_risk = {
            "scan": 5,
            "exploit": 15,
            "download": 10,
            "hack": 20
        }.get(action, 5)
        
        # Adjust risk based on player skills
        skill_modifier = sum(self.player.skills.values()) / len(self.player.skills)
        adjusted_risk = base_risk * (1 - (skill_modifier * 0.1))
        
        # Add some randomness
        final_risk = max(1, min(100, int(adjusted_risk + random.randint(-5, 5))))
        
        return {
            "action": action,
            "base_risk": base_risk,
            "skill_modifier": skill_modifier,
            "final_risk": final_risk
        } 