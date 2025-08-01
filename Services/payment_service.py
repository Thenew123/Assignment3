from Config.database_config import DatabaseConfig
from datetime import datetime

class PaymentService:
    def __init__(self):
        self.db = DatabaseConfig().create_connection()

    def process_payment(self, order_id, method_id, amount, reference=None):
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO payment (
                order_id, payment_method_id, payment_amount, transaction_reference, payment_status
            )
            VALUES (?, ?, ?, ?, 'Completed')
        """, (order_id, method_id, amount, reference))
        self.db.commit()
        payment_id = cursor.lastrowid
        return {
            "success": True,
            "payment_id": payment_id
        }


    def get_payment(self, order_id):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT payment_id, payment_amount, payment_status, payment_date
            FROM payment
            WHERE order_id = ?
        """, (order_id,))
        return cursor.fetchone()

    def get_methods(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT payment_method_id, method_type FROM payment_method")
        return cursor.fetchall()
