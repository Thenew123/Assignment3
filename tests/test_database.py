# tests/test_database.py
import pytest

from Config.database_config import DatabaseConfig

def test_connection():
    db_config = DatabaseConfig()
    conn = db_config.create_connection()
    assert conn is not None
    conn.close()

def test_tables_exist():
    db_config = DatabaseConfig()
    conn = db_config.create_connection()
    cursor = conn.cursor()
    tables = ['customer', 'staff', 'product', 'inventory', 'orders', 'cart', 'payment']
    for table in tables:
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        assert cursor.fetchone() is not None, f"Table {table} should exist"
    conn.close()

