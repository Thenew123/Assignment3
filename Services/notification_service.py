from Config.database_config import DatabaseConfig
from datetime import datetime

class NotificationService:
    def __init__(self):
        self.db = DatabaseConfig().create_connection()

    def send_notification(self, customer_id, message, notification_type='General', order_id=None, delivery_method='In_App'):
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO notification (
                customer_id, order_id, notification_type,
                message, sent_date, is_read, delivery_method
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            customer_id, order_id, notification_type,
            message, datetime.now(), 0, delivery_method
        ))
        self.db.commit()
        return cursor.lastrowid

    def mark_as_read(self, notification_id):
        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE notification SET is_read = 1 WHERE notification_id = ?
        """, (notification_id,))
        self.db.commit()
        return cursor.rowcount > 0

    def get_customer_notifications(self, customer_id, unread_only=False):
        cursor = self.db.cursor()
        query = """
            SELECT notification_id, message, sent_date, is_read
            FROM notification
            WHERE customer_id = ?
        """
        if unread_only:
            query += " AND is_read = 0"
        query += " ORDER BY sent_date DESC"
        cursor.execute(query, (customer_id,))
        return cursor.fetchall()
