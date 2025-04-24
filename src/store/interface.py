"""Store interface module."""

from typing import Dict, List, Optional
from .store import Store
from src.core.player import Player
from src.ui.terminal import TerminalUI

class StoreInterface:
    """Manages the store interface and user interaction."""
    
    def __init__(self, player: Player, ui: TerminalUI):
        """Initialize the store interface.
        
        Args:
            player: Player instance
            ui: TerminalUI instance
        """
        self.player = player
        self.ui = ui
        self.store = Store()
    
    def _display_welcome(self) -> None:
        """Display the store interface welcome message."""
        self.ui.display_info("\n=== Black Market Store ===")
        self.ui.display_info("Type 'help' for available commands")
        self._display_balance()
    
    def _display_balance(self) -> None:
        """Display player's current balance."""
        self.ui.display_info(f"\nCurrent Balance: {self.player.credits} credits")
    
    def _display_help(self) -> None:
        """Display store interface help."""
        self.ui.display_info("\nAvailable Commands:")
        self.ui.display_info("- list: List available items")
        self.ui.display_info("- buy <item_id>: Buy an item")
        self.ui.display_info("- sell <item_id>: Sell an item")
        self.ui.display_info("- inventory: Show your inventory")
        self.ui.display_info("- refresh: Refresh store stock")
        self.ui.display_info("- help: Show this help")
        self.ui.display_info("- exit: Exit store")
    
    def _display_items(self) -> None:
        """Display available items."""
        items = self.store.get_available_items(self.player.skills, self.player.level)
        
        if not items:
            self.ui.display_info("No items available for your level and skills.")
            return
        
        self.ui.display_info("\nAvailable Items:")
        for item in items:
            self.ui.display_info(f"\n{item['name']} (ID: {item['id']})")
            self.ui.display_info(f"Description: {item['description']}")
            self.ui.display_info(f"Price: {item['price']} credits")
            self.ui.display_info(f"Type: {item['type']}")
            self.ui.display_info(f"Effects: {', '.join(f'{k} +{v}' for k, v in item['effects'].items())}")
            if item['requirements']:
                self.ui.display_info(f"Requirements: {', '.join(f'{k} {v}' for k, v in item['requirements'].items())}")
            self.ui.display_info(f"Level Required: {item['level_requirement']}")
            if item['stock'] > 1:
                self.ui.display_info(f"Stock: {item['stock']}")
    
    def _display_inventory(self) -> None:
        """Display player's inventory."""
        if not self.player.inventory:
            self.ui.display_info("Your inventory is empty.")
            return
        
        self.ui.display_info("\nInventory:")
        for item_id in self.player.inventory:
            item = next((i for i in self.store.items if i.id == item_id), None)
            if item:
                self.ui.display_info(f"\n{item.name}")
                self.ui.display_info(f"Description: {item.description}")
                self.ui.display_info(f"Type: {item.type}")
                self.ui.display_info(f"Effects: {', '.join(f'{k} +{v}' for k, v in item.effects.items())}")
                if item.is_equipped:
                    self.ui.display_info("Status: Equipped")
    
    def handle_command(self, command: str) -> bool:
        """Handle a store interface command.
        
        Args:
            command: Command to handle
            
        Returns:
            bool: True if should continue, False to exit
        """
        if command.lower() == "help":
            self._display_help()
        elif command.lower() == "list":
            self._display_items()
        elif command.lower().startswith("buy "):
            self._handle_buy(command[4:].strip())
        elif command.lower().startswith("sell "):
            self._handle_sell(command[5:].strip())
        elif command.lower() == "inventory":
            self._display_inventory()
        elif command.lower() == "refresh":
            self._handle_refresh()
        elif command.lower() == "exit":
            return False
        else:
            self.ui.display_error(f"Unknown command: {command}")
        
        return True
    
    def _handle_buy(self, item_id: str) -> None:
        """Handle the buy command.
        
        Args:
            item_id: ID of the item to buy
        """
        item = self.store.buy_item(item_id, self.player.credits)
        if not item:
            self.ui.display_error("Failed to buy item. Check your credits and requirements.")
            return
        
        self.player.credits -= item.price
        self.player.add_to_inventory(item.id)
        self.ui.display_success(f"Successfully bought {item.name}")
        self._display_balance()
    
    def _handle_sell(self, item_id: str) -> None:
        """Handle the sell command.
        
        Args:
            item_id: ID of the item to sell
        """
        if item_id not in self.player.inventory:
            self.ui.display_error("Item not found in inventory.")
            return
        
        item = next((i for i in self.store.items if i.id == item_id), None)
        if not item:
            self.ui.display_error("Item not found in store.")
            return
        
        sell_price = self.store.sell_item(item)
        self.player.credits += sell_price
        self.player.remove_from_inventory(item.id)
        self.ui.display_success(f"Successfully sold {item.name} for {sell_price} credits")
        self._display_balance()
    
    def _handle_refresh(self) -> None:
        """Handle the refresh command."""
        self.store.refresh_stock()
        self.ui.display_success("Store stock refreshed")
        self._display_items()
    
    def start(self) -> None:
        """Start the store interface."""
        self._display_welcome()
        self._display_items()
        
        while True:
            command = self.ui.display_prompt()
            if not self.handle_command(command):
                break 