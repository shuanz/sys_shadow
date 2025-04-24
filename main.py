#!/usr/bin/env python3
"""
Terminal Hacker RPG - Main Game File
"""

import os
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

def display_welcome():
    """Display the welcome screen."""
    console.print(Panel.fit(
        "[bold green]Terminal Hacker RPG[/bold green]\n"
        "Welcome to the cyberpunk world of hacking!",
        title="Welcome",
        border_style="green"
    ))

def main():
    """Main game loop."""
    display_welcome()
    
    while True:
        command = Prompt.ask("\nh4ck3r@voidnet:~$")
        
        if command.lower() == "exit":
            console.print("[yellow]Logging out...[/yellow]")
            break
        elif command.lower() == "help":
            console.print("""
Available commands:
- ls: List files
- cd: Change directory
- cat: View file contents
- mail: Check messages
- bank: Check balance
- hack: Start hacking
- store: Access store
- help: Show this help
- exit: Quit game
            """)
        else:
            console.print(f"[red]Command not recognized: {command}[/red]")

if __name__ == "__main__":
    main() 