"""Hacking interface module."""

from typing import Dict, List, Optional
from .simulation import HackingSimulation
from src.core.player import Player
from src.ui.terminal import TerminalUI

class HackingInterface:
    """Manages the hacking interface and user interaction."""
    
    def __init__(self, player: Player, ui: TerminalUI):
        """Initialize the hacking interface.
        
        Args:
            player: Player instance
            ui: TerminalUI instance
        """
        self.player = player
        self.ui = ui
        self.simulation: Optional[HackingSimulation] = None
    
    def start_hacking(self, difficulty: int) -> None:
        """Start a new hacking simulation.
        
        Args:
            difficulty: Mission difficulty level
        """
        self.simulation = HackingSimulation(difficulty)
        self._display_welcome()
    
    def _display_welcome(self) -> None:
        """Display the hacking interface welcome message."""
        self.ui.display_info("\n=== Hacking Interface ===")
        self.ui.display_info("Type 'help' for available commands")
        self._display_current_status()
    
    def _display_current_status(self) -> None:
        """Display current hacking status."""
        if not self.simulation:
            return
            
        # Display current step
        step = self.simulation.get_current_step()
        if step:
            self.ui.display_info(f"\nCurrent Step: {step.name}")
            self.ui.display_info(f"Description: {step.description}")
            self.ui.display_info(f"Required Skills: {', '.join(f'{k} {v}' for k, v in step.required_skills.items())}")
        
        # Display security systems
        self.ui.display_info("\nSecurity Systems:")
        for system in self.simulation.get_security_status():
            status = "Active" if system["is_active"] else "Inactive"
            self.ui.display_info(f"- {system['name']} (Level {system['level']}) - {status}")
        
        # Display progress
        progress = self.simulation.get_progress()
        self.ui.display_info(f"\nProgress: {progress['current_step']}/{progress['total_steps']} steps")
        self.ui.display_info(f"Trace Level: {progress['trace_level']}%")
    
    def _display_help(self) -> None:
        """Display hacking interface help."""
        self.ui.display_info("\nAvailable Commands:")
        self.ui.display_info("- scan: Scan the target system")
        self.ui.display_info("- hack: Attempt current hacking step")
        self.ui.display_info("- status: Show current status")
        self.ui.display_info("- systems: List security systems")
        self.ui.display_info("- exit: Exit hacking interface")
    
    def handle_command(self, command: str) -> bool:
        """Handle a hacking interface command.
        
        Args:
            command: Command to handle
            
        Returns:
            bool: True if should continue, False to exit
        """
        if not self.simulation:
            return False
            
        if command.lower() == "help":
            self._display_help()
        elif command.lower() == "scan":
            self._handle_scan()
        elif command.lower() == "hack":
            self._handle_hack()
        elif command.lower() == "status":
            self._display_current_status()
        elif command.lower() == "systems":
            self._display_systems()
        elif command.lower() == "exit":
            return False
        else:
            self.ui.display_error(f"Unknown command: {command}")
        
        return True
    
    def _handle_scan(self) -> None:
        """Handle the scan command."""
        if not self.simulation:
            return
            
        self.ui.display_info("\nScanning target system...")
        systems = self.simulation.get_security_status()
        
        self.ui.display_info("\nScan Results:")
        for system in systems:
            if system["is_active"]:
                self.ui.display_info(f"- {system['name']} detected")
                self.ui.display_info(f"  Level: {system['level']}")
                self.ui.display_info(f"  Detection Chance: {system['detection_chance']*100:.1f}%")
        
        # Increase trace level slightly for scanning
        self.simulation.trace_level += 2
        self.ui.display_info(f"\nTrace Level: {self.simulation.trace_level}%")
    
    def _handle_hack(self) -> None:
        """Handle the hack command."""
        if not self.simulation:
            return
            
        step = self.simulation.get_current_step()
        if not step:
            self.ui.display_info("No more steps available")
            return
        
        self.ui.display_info(f"\nAttempting {step.name}...")
        success, message, trace_increase = self.simulation.attempt_step(self.player.skills)
        
        if success:
            self.ui.display_success(message)
        else:
            self.ui.display_error(message)
        
        self.ui.display_info(f"Trace Level: {self.simulation.trace_level}%")
        
        if self.simulation.is_complete():
            self.ui.display_success("\nHacking completed successfully!")
            return False
        
        return True
    
    def _display_systems(self) -> None:
        """Display detailed security system information."""
        if not self.simulation:
            return
            
        self.ui.display_info("\nSecurity Systems:")
        for system in self.simulation.security_systems:
            self.ui.display_info(f"\n{system.name}:")
            self.ui.display_info(f"Level: {system.level}")
            self.ui.display_info(f"Status: {'Active' if system.is_active else 'Inactive'}")
            self.ui.display_info(f"Detection Chance: {system.detection_chance*100:.1f}%")
            self.ui.display_info("Vulnerabilities:")
            for vuln in system.vulnerabilities:
                self.ui.display_info(f"- {vuln}") 