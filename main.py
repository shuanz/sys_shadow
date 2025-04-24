#!/usr/bin/env python3
"""
Terminal Hacker RPG - Main Game File
"""

import os
import sys
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text

class TerminalHackerRPG:
    def __init__(self):
        self.console = Console()
        self.running = True
        self.current_directory = "~"
        self.prompt = "h4ck3r@voidnet:~$"

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_welcome(self):
        welcome_text = Text()
        welcome_text.append("Terminal Hacker RPG\n", style="bold green")
        welcome_text.append("Bem-vindo ao mundo cyberpunk!\n", style="cyan")
        welcome_text.append("Digite 'help' para ver os comandos disponíveis.", style="yellow")
        
        self.console.print(Panel(welcome_text, title="Terminal Hacker RPG", border_style="green"))

    def process_command(self, command):
        if command == "help":
            self.show_help()
        elif command == "exit":
            self.running = False
        else:
            self.console.print(f"[red]Comando não reconhecido: {command}[/red]")

    def show_help(self):
        help_text = """
        Comandos disponíveis:
        - ls: Listar arquivos
        - cd: Mudar diretório
        - cat: Ler arquivo
        - mail: Ver mensagens
        - bank: Ver saldo
        - hack: Iniciar invasão
        - store: Acessar loja
        - help: Mostrar ajuda
        - exit: Sair do jogo
        """
        self.console.print(Panel(help_text, title="Ajuda", border_style="blue"))

    def run(self):
        self.clear_screen()
        self.show_welcome()
        
        while self.running:
            try:
                command = Prompt.ask(f"\n{self.prompt}")
                self.process_command(command.strip())
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Use 'exit' para sair do jogo[/yellow]")
            except Exception as e:
                self.console.print(f"[red]Erro: {str(e)}[/red]")

if __name__ == "__main__":
    game = TerminalHackerRPG()
    game.run() 