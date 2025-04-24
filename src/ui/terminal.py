"""Terminal UI components for the game."""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.style import Style
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from rich import box

class TerminalUI:
    """Main terminal UI class with cyberpunk aesthetics."""
    
    def __init__(self):
        """Initialize the terminal UI."""
        self.console = Console()
        self.style = Style(color="green", bold=True)
        self.prompt_style = Style(color="green", bold=True)
        self.error_style = Style(color="red", bold=True)
        self.success_style = Style(color="green", bold=True)
        self.info_style = Style(color="cyan", bold=True)
        
    def display_welcome(self):
        """Display the welcome screen."""
        welcome_text = Text()
        welcome_text.append("Terminal Hacker RPG\n", style=self.style)
        welcome_text.append("Welcome to the cyberpunk world of hacking!", style=self.info_style)
        
        self.console.print(Panel.fit(
            welcome_text,
            title="Welcome",
            border_style="green",
            box=box.DOUBLE
        ))
    
    def display_prompt(self):
        """Display the command prompt."""
        self.console.print("\nh4ck3r@voidnet:~$", style=self.prompt_style, end="")
        return input()
    
    def display_error(self, message: str):
        """Display an error message."""
        self.console.print(f"[red]Error: {message}[/red]", style=self.error_style)
    
    def display_success(self, message: str):
        """Display a success message."""
        self.console.print(f"[green]{message}[/green]", style=self.success_style)
    
    def display_info(self, message: str):
        """Display an info message."""
        self.console.print(f"[cyan]{message}[/cyan]", style=self.info_style)
    
    def display_help(self):
        """Display the help menu."""
        help_table = Table(show_header=True, header_style="bold green", box=box.DOUBLE)
        help_table.add_column("Command", style="green")
        help_table.add_column("Description", style="cyan")
        
        commands = [
            ("ls", "List files"),
            ("cd", "Change directory"),
            ("cat", "View file contents"),
            ("mail", "Check messages"),
            ("bank", "Check balance"),
            ("hack", "Start hacking"),
            ("store", "Access store"),
            ("help", "Show this help"),
            ("exit", "Quit game")
        ]
        
        for cmd, desc in commands:
            help_table.add_row(cmd, desc)
        
        self.console.print(help_table)
    
    def display_file_list(self, files: list):
        """Display a list of files."""
        file_table = Table(show_header=True, header_style="bold green", box=box.DOUBLE)
        file_table.add_column("Name", style="green")
        file_table.add_column("Size", style="cyan")
        file_table.add_column("Type", style="yellow")
        
        for file in files:
            file_table.add_row(file["name"], file["size"], file["type"])
        
        self.console.print(file_table)
    
    def display_file_content(self, content: str):
        """Display file content."""
        self.console.print(Panel(
            content,
            title="File Content",
            border_style="green",
            box=box.DOUBLE
        ))
    
    def display_status_bar(self, status: dict):
        """Display the status bar."""
        status_text = Text()
        status_text.append(f"Credits: {status.get('credits', 0)} | ", style="green")
        status_text.append(f"Level: {status.get('level', 1)} | ", style="cyan")
        status_text.append(f"Trace: {status.get('trace', 0)}%", style="yellow")
        
        self.console.print(Panel(
            status_text,
            title="Status",
            border_style="green",
            box=box.DOUBLE
        )) 