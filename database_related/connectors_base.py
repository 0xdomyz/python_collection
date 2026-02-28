"""Base database connection classes for reuse across notebooks."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
import sqlite3

class DatabaseConnector(ABC):
    """Abstract base for database connections."""
    
    @abstractmethod
    def connect(self):
        """Establish database connection."""
        pass
    
    @abstractmethod
    def run(self, query: str):
        """Execute query and return results."""
        pass
    
    def close(self):
        """Close connection."""
        pass


class SQLiteConnector(DatabaseConnector):
    """SQLite connection wrapper."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Connect to SQLite database."""
        self.conn = sqlite3.connect(self.db_path)
        return self.conn
    
    def run(self, query: str):
        """Execute query."""
        if self.conn is None:
            self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        return cursor.fetchall()
    
    def close(self):
        """Close connection."""
        if self.conn:
            self.conn.close()