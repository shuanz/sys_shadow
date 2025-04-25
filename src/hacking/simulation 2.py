"""Hacking simulation module."""

from typing import Dict, List, Optional, Tuple
import random
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SecuritySystem:
    """Represents a security system in the target."""
    name: str
    level: int
    vulnerabilities: List[str]
    is_active: bool = True
    detection_chance: float = 0.0
    
    def __post_init__(self):
        """Initialize detection chance based on level."""
        self.detection_chance = 0.1 * self.level

@dataclass
class HackingStep:
    """Represents a step in the hacking process."""
    name: str
    description: str
    required_skills: Dict[str, int]
    success_chance: float
    trace_increase: int
    time_cost: int

class HackingSimulation:
    """Simulates the hacking process in missions."""
    
    def __init__(self, difficulty: int):
        """Initialize the hacking simulation.
        
        Args:
            difficulty: Mission difficulty level
        """
        self.difficulty = difficulty
        self.current_step = 0
        self.completed_steps = []
        self.trace_level = 0
        self.security_systems = self._generate_security_systems()
        self.hacking_steps = self._generate_hacking_steps()
    
    def _generate_security_systems(self) -> List[SecuritySystem]:
        """Generate security systems for the target.
        
        Returns:
            List[SecuritySystem]: List of security systems
        """
        systems = [
            SecuritySystem(
                name="Firewall",
                level=max(1, self.difficulty - 1),
                vulnerabilities=["port_scan", "protocol_weakness", "misconfiguration"]
            ),
            SecuritySystem(
                name="Intrusion Detection",
                level=max(1, self.difficulty - 2),
                vulnerabilities=["false_positive", "protocol_weakness", "resource_exhaustion"]
            ),
            SecuritySystem(
                name="Access Control",
                level=self.difficulty,
                vulnerabilities=["weak_passwords", "privilege_escalation", "session_hijacking"]
            ),
            SecuritySystem(
                name="Encryption",
                level=max(1, self.difficulty - 1),
                vulnerabilities=["weak_algorithm", "key_management", "implementation_flaw"]
            )
        ]
        
        # Randomly activate systems based on difficulty
        for system in systems:
            system.is_active = random.random() < (0.5 + (self.difficulty * 0.05))
        
        return systems
    
    def _generate_hacking_steps(self) -> List[HackingStep]:
        """Generate hacking steps for the mission.
        
        Returns:
            List[HackingStep]: List of hacking steps
        """
        return [
            HackingStep(
                name="Initial Scan",
                description="Scan the target system for vulnerabilities",
                required_skills={"networking": 1, "hacking": 1},
                success_chance=0.8,
                trace_increase=5,
                time_cost=10
            ),
            HackingStep(
                name="Firewall Bypass",
                description="Attempt to bypass the firewall",
                required_skills={"hacking": 2, "stealth": 1},
                success_chance=0.7,
                trace_increase=10,
                time_cost=15
            ),
            HackingStep(
                name="System Access",
                description="Gain access to the target system",
                required_skills={"hacking": 3, "programming": 2},
                success_chance=0.6,
                trace_increase=15,
                time_cost=20
            ),
            HackingStep(
                name="Data Extraction",
                description="Extract sensitive data from the system",
                required_skills={"hacking": 4, "stealth": 3},
                success_chance=0.5,
                trace_increase=20,
                time_cost=25
            ),
            HackingStep(
                name="Cover Tracks",
                description="Remove evidence of the intrusion",
                required_skills={"hacking": 3, "stealth": 4},
                success_chance=0.7,
                trace_increase=5,
                time_cost=15
            )
        ]
    
    def get_current_step(self) -> Optional[HackingStep]:
        """Get the current hacking step.
        
        Returns:
            Optional[HackingStep]: Current step or None if completed
        """
        if self.current_step >= len(self.hacking_steps):
            return None
        return self.hacking_steps[self.current_step]
    
    def get_security_status(self) -> List[Dict]:
        """Get the status of security systems.
        
        Returns:
            List[Dict]: List of security system statuses
        """
        return [
            {
                "name": system.name,
                "level": system.level,
                "is_active": system.is_active,
                "detection_chance": system.detection_chance
            }
            for system in self.security_systems
        ]
    
    def attempt_step(self, player_skills: Dict[str, int]) -> Tuple[bool, str, int]:
        """Attempt the current hacking step.
        
        Args:
            player_skills: Player's skill levels
            
        Returns:
            Tuple[bool, str, int]: (success, message, trace_increase)
        """
        step = self.get_current_step()
        if not step:
            return False, "No more steps available", 0
        
        # Check if player meets requirements
        for skill, level in step.required_skills.items():
            if player_skills.get(skill, 0) < level:
                return False, f"Insufficient {skill} skill level", 0
        
        # Calculate success chance
        base_chance = step.success_chance
        skill_bonus = sum(
            (player_skills.get(skill, 0) - level) * 0.05
            for skill, level in step.required_skills.items()
        )
        final_chance = min(0.95, base_chance + skill_bonus)
        
        # Attempt the step
        success = random.random() < final_chance
        
        if success:
            self.completed_steps.append(step.name)
            self.current_step += 1
            message = f"Successfully completed {step.name}"
        else:
            message = f"Failed to complete {step.name}"
        
        # Calculate trace increase
        trace_increase = step.trace_increase
        if not success:
            trace_increase *= 2  # Double trace increase on failure
        
        # Check security systems
        for system in self.security_systems:
            if system.is_active and random.random() < system.detection_chance:
                trace_increase += int(system.detection_chance * 10)
        
        self.trace_level += trace_increase
        
        return success, message, trace_increase
    
    def is_complete(self) -> bool:
        """Check if the hacking simulation is complete.
        
        Returns:
            bool: True if all steps are completed
        """
        return self.current_step >= len(self.hacking_steps)
    
    def get_progress(self) -> Dict:
        """Get the current progress of the hacking simulation.
        
        Returns:
            Dict: Progress information
        """
        return {
            "current_step": self.current_step,
            "total_steps": len(self.hacking_steps),
            "completed_steps": self.completed_steps,
            "trace_level": self.trace_level
        } 