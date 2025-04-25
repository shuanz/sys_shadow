"""Multiplayer system module for local/LAN gameplay."""

from typing import Dict, List, Optional
from .player import Player
import json
import os
from datetime import datetime
import socket
import threading
import queue
import time
import pickle

class MultiplayerSystem:
    """Manages multiplayer functionality for local/LAN gameplay."""
    
    def __init__(self, player: Player):
        """Initialize the multiplayer system.
        
        Args:
            player: The player instance
        """
        self.player = player
        self.players: Dict[str, Dict] = {}
        self.game_sessions: Dict[str, Dict] = {}
        self.active_session: Optional[str] = None
        self.connection_history: List[Dict] = []
        self._load_multiplayer_data()
        
        # Network settings
        self.host = "localhost"
        self.port = 5001
        self.server_socket = None
        self.is_server_running = False
        
        # Message queues for each player
        self.message_queues: Dict[str, queue.Queue] = {}
    
    def start_server(self) -> bool:
        """Start the multiplayer server.
        
        Returns:
            bool: True if server started successfully
        """
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.is_server_running = True
            
            # Start server thread
            server_thread = threading.Thread(target=self._handle_connections)
            server_thread.daemon = True
            server_thread.start()
            
            return True
        except Exception:
            return False
    
    def stop_server(self) -> None:
        """Stop the multiplayer server."""
        self.is_server_running = False
        if self.server_socket:
            self.server_socket.close()
    
    def _handle_connections(self) -> None:
        """Handle incoming player connections."""
        while self.is_server_running:
            try:
                client_socket, address = self.server_socket.accept()
                player_id = f"player_{len(self.players)}"
                
                # Create new player connection
                self.players[player_id] = {
                    "id": player_id,
                    "address": address,
                    "socket": client_socket,
                    "connected_at": datetime.now().isoformat(),
                    "status": "connected"
                }
                
                # Create message queue for player
                self.message_queues[player_id] = queue.Queue()
                
                # Start player handler thread
                player_thread = threading.Thread(
                    target=self._handle_player,
                    args=(player_id,)
                )
                player_thread.daemon = True
                player_thread.start()
                
                self._record_connection_event(player_id, "connect", address)
            except Exception:
                continue
    
    def _handle_player(self, player_id: str) -> None:
        """Handle a player connection.
        
        Args:
            player_id: ID of the player
        """
        player = self.players.get(player_id)
        if not player:
            return
            
        client_socket = player["socket"]
        message_queue = self.message_queues[player_id]
        
        try:
            while player["status"] == "connected":
                # Check for messages to send
                try:
                    message = message_queue.get_nowait()
                    client_socket.send(pickle.dumps(message))
                except queue.Empty:
                    pass
                
                # Check for incoming messages
                try:
                    data = client_socket.recv(4096)
                    if data:
                        message = pickle.loads(data)
                        self._handle_message(player_id, message)
                except socket.error:
                    break
                
                time.sleep(0.1)
        except Exception:
            pass
        finally:
            self._close_player_connection(player_id)
    
    def _close_player_connection(self, player_id: str) -> None:
        """Close a player connection.
        
        Args:
            player_id: ID of the player
        """
        player = self.players.get(player_id)
        if not player:
            return
            
        try:
            player["socket"].close()
        except Exception:
            pass
            
        player["status"] = "disconnected"
        player["disconnected_at"] = datetime.now().isoformat()
        
        self._record_connection_event(player_id, "disconnect", player["address"])
        self._save_multiplayer_data()
    
    def _handle_message(self, player_id: str, message: Dict) -> None:
        """Handle a message from a player.
        
        Args:
            player_id: ID of the player
            message: Message content
        """
        message_type = message.get("type")
        
        if message_type == "join_session":
            self._handle_join_session(player_id, message)
        elif message_type == "leave_session":
            self._handle_leave_session(player_id, message)
        elif message_type == "game_action":
            self._handle_game_action(player_id, message)
        elif message_type == "chat":
            self._handle_chat_message(player_id, message)
    
    def _handle_join_session(self, player_id: str, message: Dict) -> None:
        """Handle a player joining a game session.
        
        Args:
            player_id: ID of the player
            message: Join session message
        """
        session_id = message.get("session_id")
        if not session_id:
            return
            
        if session_id not in self.game_sessions:
            self.game_sessions[session_id] = {
                "id": session_id,
                "players": [],
                "created_at": datetime.now().isoformat(),
                "status": "active"
            }
        
        self.game_sessions[session_id]["players"].append(player_id)
        self._broadcast_to_session(session_id, {
            "type": "player_joined",
            "player_id": player_id,
            "session_id": session_id
        })
    
    def _handle_leave_session(self, player_id: str, message: Dict) -> None:
        """Handle a player leaving a game session.
        
        Args:
            player_id: ID of the player
            message: Leave session message
        """
        session_id = message.get("session_id")
        if not session_id or session_id not in self.game_sessions:
            return
            
        if player_id in self.game_sessions[session_id]["players"]:
            self.game_sessions[session_id]["players"].remove(player_id)
            
        self._broadcast_to_session(session_id, {
            "type": "player_left",
            "player_id": player_id,
            "session_id": session_id
        })
    
    def _handle_game_action(self, player_id: str, message: Dict) -> None:
        """Handle a game action from a player.
        
        Args:
            player_id: ID of the player
            message: Game action message
        """
        session_id = message.get("session_id")
        if not session_id or session_id not in self.game_sessions:
            return
            
        self._broadcast_to_session(session_id, {
            "type": "game_action",
            "player_id": player_id,
            "action": message.get("action"),
            "data": message.get("data")
        })
    
    def _handle_chat_message(self, player_id: str, message: Dict) -> None:
        """Handle a chat message from a player.
        
        Args:
            player_id: ID of the player
            message: Chat message
        """
        session_id = message.get("session_id")
        if not session_id or session_id not in self.game_sessions:
            return
            
        self._broadcast_to_session(session_id, {
            "type": "chat",
            "player_id": player_id,
            "message": message.get("message")
        })
    
    def _broadcast_to_session(self, session_id: str, message: Dict) -> None:
        """Broadcast a message to all players in a session.
        
        Args:
            session_id: ID of the session
            message: Message to broadcast
        """
        if session_id not in self.game_sessions:
            return
            
        for player_id in self.game_sessions[session_id]["players"]:
            self.send_message(player_id, message)
    
    def send_message(self, player_id: str, message: Dict) -> bool:
        """Send a message to a player.
        
        Args:
            player_id: ID of the player
            message: Message to send
            
        Returns:
            bool: True if message was sent successfully
        """
        if player_id not in self.players:
            return False
            
        message_queue = self.message_queues.get(player_id)
        if not message_queue:
            return False
            
        try:
            message_queue.put(message)
            return True
        except Exception:
            return False
    
    def get_player_status(self, player_id: str) -> Dict:
        """Get the status of a player.
        
        Args:
            player_id: ID of the player
            
        Returns:
            Dict: Player status information
        """
        if player_id not in self.players:
            return {}
            
        player = self.players[player_id]
        return {
            "id": player["id"],
            "address": player["address"],
            "status": player["status"],
            "connected_at": player["connected_at"],
            "disconnected_at": player.get("disconnected_at")
        }
    
    def get_all_player_status(self) -> List[Dict]:
        """Get status of all players.
        
        Returns:
            List[Dict]: List of player statuses
        """
        return [
            self.get_player_status(player_id)
            for player_id in self.players.keys()
        ]
    
    def get_session_status(self, session_id: str) -> Dict:
        """Get the status of a game session.
        
        Args:
            session_id: ID of the session
            
        Returns:
            Dict: Session status information
        """
        if session_id not in self.game_sessions:
            return {}
            
        session = self.game_sessions[session_id]
        return {
            "id": session["id"],
            "players": session["players"],
            "status": session["status"],
            "created_at": session["created_at"]
        }
    
    def get_all_session_status(self) -> List[Dict]:
        """Get status of all game sessions.
        
        Returns:
            List[Dict]: List of session statuses
        """
        return [
            self.get_session_status(session_id)
            for session_id in self.game_sessions.keys()
        ]
    
    def _record_connection_event(self, player_id: str, event_type: str, address: tuple) -> None:
        """Record a connection event.
        
        Args:
            player_id: ID of the player
            event_type: Type of event
            address: Connection address
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "player_id": player_id,
            "type": event_type,
            "address": address
        }
        self.connection_history.append(event)
    
    def get_connection_history(self, limit: int = 10) -> List[Dict]:
        """Get recent connection history.
        
        Args:
            limit: Maximum number of events to return
            
        Returns:
            List[Dict]: Recent connection events
        """
        return self.connection_history[-limit:]
    
    def _save_multiplayer_data(self) -> None:
        """Save multiplayer data to a file."""
        save_data = {
            "players": self.players,
            "game_sessions": self.game_sessions,
            "connection_history": self.connection_history,
            "last_updated": datetime.now().isoformat()
        }
        
        with open("multiplayer_data.json", "w") as f:
            json.dump(save_data, f, indent=4)
    
    def _load_multiplayer_data(self) -> None:
        """Load multiplayer data from a file."""
        if not os.path.exists("multiplayer_data.json"):
            return
            
        try:
            with open("multiplayer_data.json", "r") as f:
                save_data = json.load(f)
                self.players = save_data.get("players", {})
                self.game_sessions = save_data.get("game_sessions", {})
                self.connection_history = save_data.get("connection_history", [])
        except Exception:
            pass 