"""File system simulation module."""

from typing import Dict, List, Optional
import os
import json
import random
from dataclasses import dataclass
from datetime import datetime

@dataclass
class FileNode:
    """Represents a file or directory in the virtual file system."""
    name: str
    is_directory: bool
    content: Optional[str] = None
    size: int = 0
    created_at: str = ""
    modified_at: str = ""
    children: Dict[str, 'FileNode'] = None
    
    def __post_init__(self):
        """Initialize children dictionary for directories."""
        if self.is_directory and self.children is None:
            self.children = {}
        
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.modified_at:
            self.modified_at = self.created_at

class FileSystem:
    """Virtual file system for the game."""
    
    def __init__(self):
        """Initialize the file system."""
        self.root = FileNode("/", True)
        self.current_path = "/"
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialize the basic file system structure."""
        # Create home directory
        home = FileNode("home", True)
        self.root.children["home"] = home
        
        # Create system directories
        system_dirs = ["bin", "etc", "var", "usr", "tmp"]
        for dir_name in system_dirs:
            self.root.children[dir_name] = FileNode(dir_name, True)
        
        # Create some initial files
        self._create_file("/home/readme.txt", "Welcome to the Terminal Hacker RPG!\n\nThis is your home directory.")
        self._create_file("/home/notes.txt", "Important notes and reminders will appear here.")
    
    def _create_file(self, path: str, content: str) -> bool:
        """Create a new file in the system.
        
        Args:
            path: Path where to create the file
            content: Content of the file
            
        Returns:
            bool: True if file was created successfully
        """
        parts = path.strip("/").split("/")
        current = self.root
        
        # Navigate to the parent directory
        for part in parts[:-1]:
            if part not in current.children:
                return False
            current = current.children[part]
            if not current.is_directory:
                return False
        
        # Create the file
        filename = parts[-1]
        if filename in current.children:
            return False
            
        current.children[filename] = FileNode(
            name=filename,
            is_directory=False,
            content=content,
            size=len(content)
        )
        return True
    
    def _get_node(self, path: str) -> Optional[FileNode]:
        """Get a file or directory node by path.
        
        Args:
            path: Path to the node
            
        Returns:
            Optional[FileNode]: The node if found, None otherwise
        """
        if path == "/":
            return self.root
            
        parts = path.strip("/").split("/")
        current = self.root
        
        for part in parts:
            if part not in current.children:
                return None
            current = current.children[part]
            
        return current
    
    def list_directory(self, path: str = None) -> List[Dict]:
        """List contents of a directory.
        
        Args:
            path: Path to list (defaults to current directory)
            
        Returns:
            List[Dict]: List of files and directories
        """
        if path is None:
            path = self.current_path
            
        node = self._get_node(path)
        if not node or not node.is_directory:
            return []
            
        result = []
        for name, child in node.children.items():
            result.append({
                "name": name,
                "type": "dir" if child.is_directory else "file",
                "size": child.size,
                "modified": child.modified_at
            })
            
        return result
    
    def read_file(self, path: str) -> Optional[str]:
        """Read contents of a file.
        
        Args:
            path: Path to the file
            
        Returns:
            Optional[str]: File contents if found
        """
        node = self._get_node(path)
        if not node or node.is_directory:
            return None
            
        return node.content
    
    def change_directory(self, path: str) -> bool:
        """Change current directory.
        
        Args:
            path: Path to change to
            
        Returns:
            bool: True if directory was changed successfully
        """
        if path == "..":
            # Go up one level
            parts = self.current_path.strip("/").split("/")
            if len(parts) > 1:
                self.current_path = "/" + "/".join(parts[:-1])
            else:
                self.current_path = "/"
            return True
            
        # Handle absolute paths
        if path.startswith("/"):
            new_path = path
        else:
            # Handle relative paths
            new_path = os.path.normpath(os.path.join(self.current_path, path))
            if not new_path.startswith("/"):
                new_path = "/" + new_path
                
        node = self._get_node(new_path)
        if not node or not node.is_directory:
            return False
            
        self.current_path = new_path
        return True
    
    def get_current_path(self) -> str:
        """Get the current directory path.
        
        Returns:
            str: Current path
        """
        return self.current_path
    
    def generate_target_system(self, difficulty: int) -> None:
        """Generate a target system's file structure.
        
        Args:
            difficulty: System difficulty level
        """
        # Create target system directory
        target_dir = FileNode("target", True)
        self.root.children["target"] = target_dir
        
        # Generate random file structure based on difficulty
        self._generate_random_structure(target_dir, difficulty)
    
    def _generate_random_structure(self, parent: FileNode, depth: int) -> None:
        """Generate random file structure.
        
        Args:
            parent: Parent directory node
            depth: Current depth level
        """
        if depth <= 0:
            return
            
        # Generate random number of files and directories
        num_items = random.randint(3, 5 + depth)
        
        for i in range(num_items):
            is_dir = random.random() < 0.3  # 30% chance of being a directory
            name = f"item_{i}"
            
            if is_dir:
                node = FileNode(name, True)
                parent.children[name] = node
                self._generate_random_structure(node, depth - 1)
            else:
                content = f"File {name} content"
                node = FileNode(name, False, content, len(content))
                parent.children[name] = node 