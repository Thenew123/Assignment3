from Config.database_config import DatabaseConfig
from Config.app_config import LOW_STOCK_THRESHOLD
import sqlite3
from datetime import datetime

class InventoryService:
    def __init__(self):
        self.db = DatabaseConfig().create_connection()

    def get_inventory_by_branch(self, branch_id):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT i.inventory_id, p.product_name, i.quantity_in_stock, i.last_restocked
            FROM inventory i
            JOIN product p ON i.product_id = p.product_id
            WHERE i.branch_id = ?
            ORDER BY p.product_name
        """, (branch_id,))
        return cursor.fetchall()

    def update_stock(self, inventory_id, new_quantity):
        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE inventory
            SET quantity_in_stock = ?, last_restocked = ?
            WHERE inventory_id = ?
        """, (new_quantity, datetime.now().date(), inventory_id))
        self.db.commit()
        return cursor.rowcount > 0

    def add_new_inventory_item(self, branch_id, product_id, quantity):
        cursor = self.db.cursor()
        try:
            cursor.execute("""
                INSERT INTO inventory (branch_id, product_id, quantity_in_stock, last_restocked)
                VALUES (?, ?, ?, ?)
            """, (branch_id, product_id, quantity, datetime.now().date()))
            self.db.commit()
            return True, "Inventory item added successfully"
        except sqlite3.IntegrityError:
            return False, "This product already exists in the branch inventory"

    def get_low_stock_items(self, branch_id, threshold=LOW_STOCK_THRESHOLD):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT i.inventory_id, p.product_name, i.quantity_in_stock
            FROM inventory i
            JOIN product p ON i.product_id = p.product_id
            WHERE i.branch_id = ? AND i.quantity_in_stock <= ?
        """, (branch_id, threshold))
        return cursor.fetchall()
