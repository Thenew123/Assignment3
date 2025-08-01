# Models/customer.py
import sqlite3
from Config.database_config import DatabaseConfig

class Customer:
    """Customer model and database operations"""
    
    def __init__(self):
        self.db_config = DatabaseConfig()
    
    def authenticate(self, email, phone):
        """Authenticate customer with email and phone"""
        conn = self.db_config.create_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT customer_id, first_name, last_name
                FROM customer 
                WHERE email = ? AND phone = ?
            """, (email, phone))
            
            result = cursor.fetchone()
            return result
        finally:
            conn.close()
    
    def create_customer(self, first_name, last_name, email, phone, address=None, date_of_birth=None):
        """Create new customer"""
        conn = self.db_config.create_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO customer (first_name, last_name, email, phone, address, date_of_birth)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (first_name, last_name, email, phone, address, date_of_birth))
            
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None  # Customer already exists
        finally:
            conn.close()
    
    def get_customer_by_id(self, customer_id):
        """Get customer by ID"""
        conn = self.db_config.create_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT customer_id, first_name, last_name, email, phone, address, date_of_birth
                FROM customer 
                WHERE customer_id = ?
            """, (customer_id,))
            
            return cursor.fetchone()
        finally:
            conn.close()
    
    def update_customer(self, customer_id, **kwargs):
        """Update customer information"""
        conn = self.db_config.create_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['first_name', 'last_name', 'email', 'phone', 'address', 'date_of_birth']:
                fields.append(f"{key} = ?")
                values.append(value)
        
        if not fields:
            return False
        
        values.append(customer_id)
        update_sql = f"UPDATE customer SET {', '.join(fields)} WHERE customer_id = ?"
        
        try:
            cursor.execute(update_sql, values)
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def get_customer_orders(self, customer_id, limit=None):
        """Get customer's order history"""
        conn = self.db_config.create_connection()
        cursor = conn.cursor()
        
        try:
            sql = """
                SELECT o.order_id, o.order_date, o.order_status, o.total_amount,
                       b.branch_name, p.payment_status
                FROM orders o
                LEFT JOIN branch b ON o.branch_id = b.branch_id
                LEFT JOIN payment p ON o.order_id = p.order_id
                WHERE o.customer_id = ?
                ORDER BY o.order_date DESC
            """
            
            if limit:
                sql += f" LIMIT {limit}"
            
            cursor.execute(sql, (customer_id,))
            return cursor.fetchall()
        finally:
            conn.close()
    
    def get_customer_notifications(self, customer_id, unread_only=False):
        """Get customer notifications"""
        conn = self.db_config.create_connection()
        cursor = conn.cursor()
        
        try:
            sql = """
                SELECT notification_id, order_id, notification_type, message, 
                       sent_date, is_read
                FROM notification
                WHERE customer_id = ?
            """
            
            if unread_only:
                sql += " AND is_read = 0"
            
            sql += " ORDER BY sent_date DESC"
            
            cursor.execute(sql, (customer_id,))
            return cursor.fetchall()
        finally:
            conn.close()
    
    def mark_notification_read(self, notification_id):
        """Mark notification as read"""
        conn = self.db_config.create_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE notification SET is_read = 1 WHERE notification_id = ?
            """, (notification_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()