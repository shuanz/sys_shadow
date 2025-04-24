"""Mission generation module."""

from typing import Dict, List, Optional
import random
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Mission:
    """Represents a mission in the game."""
    id: str
    name: str
    description: str
    target: str
    difficulty: int
    experience_reward: int
    credit_reward: int
    time_limit: int
    required_skills: Dict[str, int]
    created_at: str = ""
    
    def __post_init__(self):
        """Initialize creation time if not provided."""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

class MissionGenerator:
    """Generates procedural missions for the game."""
    
    def __init__(self):
        """Initialize the mission generator."""
        self.corporations = [
            "Neuronet Inc.",
            "CyberCorp",
            "DataDyn",
            "TechTron",
            "Quantum Systems",
            "Binary Solutions",
            "Digital Frontiers",
            "Virtual Enterprises",
            "NetSphere",
            "CodeMatrix"
        ]
        
        self.mission_types = [
            "data_heist",
            "system_infiltration",
            "security_bypass",
            "network_breach",
            "ai_manipulation",
            "crypto_theft",
            "identity_hack",
            "system_sabotage",
            "data_leak",
            "backdoor_installation"
        ]
        
        self.mission_templates = {
            "data_heist": {
                "name": "Data Heist: {target}",
                "description": "Infiltrate {target}'s systems and extract sensitive data. Be careful not to leave traces.",
                "base_reward": 1000,
                "base_exp": 50
            },
            "system_infiltration": {
                "name": "System Infiltration: {target}",
                "description": "Gain unauthorized access to {target}'s core systems. Avoid detection at all costs.",
                "base_reward": 1500,
                "base_exp": 75
            },
            "security_bypass": {
                "name": "Security Bypass: {target}",
                "description": "Find and exploit vulnerabilities in {target}'s security systems.",
                "base_reward": 2000,
                "base_exp": 100
            },
            "network_breach": {
                "name": "Network Breach: {target}",
                "description": "Penetrate {target}'s network infrastructure and establish a persistent connection.",
                "base_reward": 2500,
                "base_exp": 125
            },
            "ai_manipulation": {
                "name": "AI Manipulation: {target}",
                "description": "Access and modify {target}'s AI systems for our benefit.",
                "base_reward": 3000,
                "base_exp": 150
            },
            "crypto_theft": {
                "name": "Crypto Theft: {target}",
                "description": "Steal cryptocurrency from {target}'s digital wallets.",
                "base_reward": 4000,
                "base_exp": 200
            },
            "identity_hack": {
                "name": "Identity Hack: {target}",
                "description": "Compromise {target}'s identity verification systems.",
                "base_reward": 3500,
                "base_exp": 175
            },
            "system_sabotage": {
                "name": "System Sabotage: {target}",
                "description": "Disrupt {target}'s operations by compromising their systems.",
                "base_reward": 5000,
                "base_exp": 250
            },
            "data_leak": {
                "name": "Data Leak: {target}",
                "description": "Extract and leak sensitive information from {target}.",
                "base_reward": 4500,
                "base_exp": 225
            },
            "backdoor_installation": {
                "name": "Backdoor Installation: {target}",
                "description": "Install a hidden backdoor in {target}'s systems for future access.",
                "base_reward": 6000,
                "base_exp": 300
            }
        }
    
    def generate_mission(self, player_level: int) -> Mission:
        """Generate a new mission based on player level.
        
        Args:
            player_level: Current player level
            
        Returns:
            Mission: Generated mission
        """
        # Select mission type and target
        mission_type = random.choice(self.mission_types)
        target = random.choice(self.corporations)
        
        # Get mission template
        template = self.mission_templates[mission_type]
        
        # Calculate difficulty and rewards
        difficulty = max(1, min(10, player_level + random.randint(-1, 2)))
        base_reward = template["base_reward"]
        base_exp = template["base_exp"]
        
        # Scale rewards based on difficulty
        credit_reward = int(base_reward * (difficulty * 0.5))
        experience_reward = int(base_exp * (difficulty * 0.5))
        
        # Generate required skills
        required_skills = {
            "hacking": max(1, difficulty - 1),
            "stealth": max(1, difficulty - 2),
            "programming": max(1, difficulty - 1),
            "networking": max(1, difficulty - 2)
        }
        
        # Generate mission ID
        mission_id = f"mission_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create mission
        return Mission(
            id=mission_id,
            name=template["name"].format(target=target),
            description=template["description"].format(target=target),
            target=target,
            difficulty=difficulty,
            experience_reward=experience_reward,
            credit_reward=credit_reward,
            time_limit=random.randint(30, 60) * difficulty,
            required_skills=required_skills
        )
    
    def get_available_missions(self, player_level: int, count: int = 3) -> List[Mission]:
        """Get a list of available missions.
        
        Args:
            player_level: Current player level
            count: Number of missions to generate
            
        Returns:
            List[Mission]: List of available missions
        """
        return [self.generate_mission(player_level) for _ in range(count)] 