from Config.database_config import DatabaseConfig

class Payment:
    def __init__(self):
        self.db = DatabaseConfig().create_connection()

    def create_payment(self, order_id, payment_method_id, amount, reference=None):
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO payment (order_id, payment_method_id, payment_amount, transaction_reference, payment_status)
            VALUES (?, ?, ?, ?, 'Completed')
        """, (order_id, payment_method_id, amount, reference))
        self.db.commit()
        return cursor.lastrowid

    def get_payment_by_order(self, order_id):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT * FROM payment
            WHERE order_id = ?
        """, (order_id,))
        return cursor.fetchone()

    def refund_payment(self, payment_id):
        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE payment
            SET payment_status = 'Refunded'
            WHERE payment_id = ?
        """, (payment_id,))
        self.db.commit()
        return cursor.rowcount > 0
