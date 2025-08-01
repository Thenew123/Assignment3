from Config.database_config import DatabaseConfig
import sqlite3
from datetime import datetime

class Order:
    def __init__(self):
        self.db = DatabaseConfig().create_connection()

    def create_order(self, customer_id, branch_id, total_amount):
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO orders (customer_id, branch_id, order_date, total_amount)
            VALUES (?, ?, ?, ?)
        """, (customer_id, branch_id, datetime.now(), total_amount))
        self.db.commit()
        return cursor.lastrowid

    def add_order_items(self, order_id, items):
        cursor = self.db.cursor()
        for item in items:
            cursor.execute("""
                INSERT INTO order_item (order_id, product_id, quantity, unit_price, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """, (order_id, item['product_id'], item['quantity'], item['unit_price'], item['subtotal']))
        self.db.commit()

    def get_order_details(self, order_id):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT * FROM orders WHERE order_id = ?
        """, (order_id,))
        return cursor.fetchone()

    def get_order_items(self, order_id):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT product_id, quantity, unit_price, subtotal
            FROM order_item WHERE order_id = ?
        """, (order_id,))
        return cursor.fetchall()

    def update_order_status(self, order_id, new_status):
        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE orders SET order_status = ? WHERE order_id = ?
        """, (new_status, order_id))
        self.db.commit()
        return cursor.rowcount > 0
