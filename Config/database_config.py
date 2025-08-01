# Config/database_config.py
import os
import sqlite3

class DatabaseConfig:
    """Database configuration and connection management"""
    
    def __init__(self, db_path='Data/pharmacy.db'):
        self.db_path = db_path
        self.ensure_db_exists()
    
    def ensure_db_exists(self):
        """Ensure database file exists"""
        if not os.path.exists(self.db_path):
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            # Create empty database
            self.create_connection().close()
    
    def create_connection(self):
        """Create and return database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    def get_db_path(self):
        """Get database path"""
        return self.db_path
    
    @staticmethod
    def check_db_exists(db_path='Data/pharmacy.db'):
        """Check if database exists"""
        return os.path.exists(db_path)
    
