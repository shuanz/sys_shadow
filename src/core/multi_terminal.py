"""Multi-terminal system module for remote sessions."""

from typing import Dict, List, Optional
from .player import Player
import json
import os
from datetime import datetime
import socket
import threading
import queue
import time

class MultiTerminal:
    """Manages multiple terminal sessions and remote connections."""
    
    def __init__(self, player: Player):
        """Initialize the multi-terminal system.
        
        Args:
            player: The player instance
        """
        self.player = player
        self.sessions: Dict[str, Dict] = {}
        self.active_session: Optional[str] = None
        self.connection_history: List[Dict] = []
        self._load_session_data()
        
        # Network settings
        self.host = "localhost"
        self.port = 5000
        self.server_socket = None
        self.is_server_running = False
        
        # Message queues for each session
        self.message_queues: Dict[str, queue.Queue] = {}
    
    def start_server(self) -> bool:
        """Start the terminal server.
        
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
        """Stop the terminal server."""
        self.is_server_running = False
        if self.server_socket:
            self.server_socket.close()
    
    def _handle_connections(self) -> None:
        """Handle incoming connections."""
        while self.is_server_running:
            try:
                client_socket, address = self.server_socket.accept()
                session_id = f"session_{len(self.sessions)}"
                
                # Create new session
                self.sessions[session_id] = {
                    "id": session_id,
                    "address": address,
                    "socket": client_socket,
                    "connected_at": datetime.now().isoformat(),
                    "status": "connected"
                }
                
                # Create message queue for session
                self.message_queues[session_id] = queue.Queue()
                
                # Start session handler thread
                session_thread = threading.Thread(
                    target=self._handle_session,
                    args=(session_id,)
                )
                session_thread.daemon = True
                session_thread.start()
                
                self._record_connection_event(session_id, "connect", address)
            except Exception:
                continue
    
    def _handle_session(self, session_id: str) -> None:
        """Handle a terminal session.
        
        Args:
            session_id: ID of the session
        """
        session = self.sessions.get(session_id)
        if not session:
            return
            
        client_socket = session["socket"]
        message_queue = self.message_queues[session_id]
        
        try:
            while session["status"] == "connected":
                # Check for messages to send
                try:
                    message = message_queue.get_nowait()
                    client_socket.send(message.encode())
                except queue.Empty:
                    pass
                
                # Check for incoming messages
                try:
                    data = client_socket.recv(1024)
                    if data:
                        self._handle_message(session_id, data.decode())
                except socket.error:
                    break
                
                time.sleep(0.1)
        except Exception:
            pass
        finally:
            self._close_session(session_id)
    
    def _close_session(self, session_id: str) -> None:
        """Close a terminal session.
        
        Args:
            session_id: ID of the session
        """
        session = self.sessions.get(session_id)
        if not session:
            return
            
        try:
            session["socket"].close()
        except Exception:
            pass
            
        session["status"] = "disconnected"
        session["disconnected_at"] = datetime.now().isoformat()
        
        self._record_connection_event(session_id, "disconnect", session["address"])
        self._save_session_data()
    
    def _handle_message(self, session_id: str, message: str) -> None:
        """Handle a message from a session.
        
        Args:
            session_id: ID of the session
            message: Message content
        """
        # TODO: Implement message handling
        pass
    
    def send_message(self, session_id: str, message: str) -> bool:
        """Send a message to a session.
        
        Args:
            session_id: ID of the session
            message: Message to send
            
        Returns:
            bool: True if message was sent successfully
        """
        if session_id not in self.sessions:
            return False
            
        message_queue = self.message_queues.get(session_id)
        if not message_queue:
            return False
            
        try:
            message_queue.put(message)
            return True
        except Exception:
            return False
    
    def get_session_status(self, session_id: str) -> Dict:
        """Get the status of a session.
        
        Args:
            session_id: ID of the session
            
        Returns:
            Dict: Session status information
        """
        if session_id not in self.sessions:
            return {}
            
        session = self.sessions[session_id]
        return {
            "id": session["id"],
            "address": session["address"],
            "status": session["status"],
            "connected_at": session["connected_at"],
            "disconnected_at": session.get("disconnected_at")
        }
    
    def get_all_session_status(self) -> List[Dict]:
        """Get status of all sessions.
        
        Returns:
            List[Dict]: List of session statuses
        """
        return [
            self.get_session_status(session_id)
            for session_id in self.sessions.keys()
        ]
    
    def _record_connection_event(self, session_id: str, event_type: str, address: tuple) -> None:
        """Record a connection event.
        
        Args:
            session_id: ID of the session
            event_type: Type of event
            address: Connection address
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
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
    
    def _save_session_data(self) -> None:
        """Save session data to a file."""
        save_data = {
            "sessions": self.sessions,
            "connection_history": self.connection_history,
            "last_updated": datetime.now().isoformat()
        }
        
        with open("session_data.json", "w") as f:
            json.dump(save_data, f, indent=4)
    
    def _load_session_data(self) -> None:
        """Load session data from a file."""
        if not os.path.exists("session_data.json"):
            return
            
        try:
            with open("session_data.json", "r") as f:
                save_data = json.load(f)
                self.sessions = save_data.get("sessions", {})
                self.connection_history = save_data.get("connection_history", [])
        except Exception:
            pass 