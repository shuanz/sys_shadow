"""LLM interface module for dynamic NPC dialogues."""

from typing import Dict, List, Optional
import os
import json
from datetime import datetime

class LLMInterface:
    """Manages the integration with Language Learning Models for dynamic NPC dialogues."""
    
    def __init__(self, model_type: str = "local"):
        """Initialize the LLM interface.
        
        Args:
            model_type: Type of LLM to use ("local" or "api")
        """
        self.model_type = model_type
        self.conversation_history: List[Dict] = []
        self._load_conversation_history()
        
        # Initialize model based on type
        if model_type == "local":
            self._initialize_local_model()
        else:
            self._initialize_api_model()
    
    def _initialize_local_model(self) -> None:
        """Initialize a local LLM model."""
        # TODO: Implement local model initialization
        # This could use Ollama, llama.cpp, or other local LLM solutions
        pass
    
    def _initialize_api_model(self) -> None:
        """Initialize an API-based LLM model."""
        # TODO: Implement API model initialization
        # This could use OpenAI, Anthropic, or other API providers
        pass
    
    def generate_response(self, prompt: str, context: Dict) -> str:
        """Generate a response from the LLM.
        
        Args:
            prompt: The input prompt
            context: Additional context for the response
            
        Returns:
            str: Generated response
        """
        # TODO: Implement actual LLM response generation
        # For now, return a placeholder response
        return f"[LLM Response] {prompt}"
    
    def generate_mission_dialogue(self, mission_data: Dict) -> str:
        """Generate mission-related dialogue.
        
        Args:
            mission_data: Mission data to use as context
            
        Returns:
            str: Generated dialogue
        """
        prompt = f"""
        Generate a mission briefing for a hacker:
        Target: {mission_data.get('target', 'Unknown')}
        Difficulty: {mission_data.get('difficulty', 1)}
        Objective: {mission_data.get('description', 'Unknown')}
        """
        
        return self.generate_response(prompt, mission_data)
    
    def generate_npc_response(self, npc_type: str, player_action: str) -> str:
        """Generate an NPC response based on player action.
        
        Args:
            npc_type: Type of NPC (e.g., "contractor", "vendor")
            player_action: Player's action or question
            
        Returns:
            str: Generated response
        """
        prompt = f"""
        Generate a response from a {npc_type}:
        Player Action: {player_action}
        """
        
        return self.generate_response(prompt, {"npc_type": npc_type})
    
    def _record_conversation(self, speaker: str, message: str) -> None:
        """Record a conversation exchange.
        
        Args:
            speaker: Who is speaking
            message: The message content
        """
        exchange = {
            "timestamp": datetime.now().isoformat(),
            "speaker": speaker,
            "message": message
        }
        self.conversation_history.append(exchange)
        self._save_conversation_history()
    
    def get_conversation_history(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation history.
        
        Args:
            limit: Maximum number of exchanges to return
            
        Returns:
            List[Dict]: Recent conversation exchanges
        """
        return self.conversation_history[-limit:]
    
    def _save_conversation_history(self) -> None:
        """Save conversation history to a file."""
        save_data = {
            "conversations": self.conversation_history,
            "last_updated": datetime.now().isoformat()
        }
        
        with open("conversation_history.json", "w") as f:
            json.dump(save_data, f, indent=4)
    
    def _load_conversation_history(self) -> None:
        """Load conversation history from a file."""
        if not os.path.exists("conversation_history.json"):
            return
            
        try:
            with open("conversation_history.json", "r") as f:
                save_data = json.load(f)
                self.conversation_history = save_data.get("conversations", [])
        except Exception:
            self.conversation_history = [] 