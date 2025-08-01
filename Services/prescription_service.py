from Config.database_config import DatabaseConfig
import sqlite3
from datetime import datetime

class PrescriptionService:
    def __init__(self):
        self.db = DatabaseConfig().create_connection()

    def validate_prescription(self, prescription_id, pharmacist_id, notes=None):
        cursor = self.db.cursor()

        cursor.execute("""
            UPDATE prescription
            SET validation_status = 'Validated',
                validation_date = ?,
                pharmacist_id = ?,
                notes = ?
            WHERE prescription_id = ?
        """, (datetime.now(), pharmacist_id, notes, prescription_id))

        self.db.commit()
        return cursor.rowcount > 0

    def reject_prescription(self, prescription_id, pharmacist_id, notes=None):
        cursor = self.db.cursor()

        cursor.execute("""
            UPDATE prescription
            SET validation_status = 'Rejected',
                validation_date = ?,
                pharmacist_id = ?,
                notes = ?
            WHERE prescription_id = ?
        """, (datetime.now(), pharmacist_id, notes, prescription_id))

        self.db.commit()
        return cursor.rowcount > 0

    def get_pending_prescriptions(self, branch_id=None):
        cursor = self.db.cursor()

        query = """
            SELECT p.prescription_id, p.prescription_number, o.order_id,
                   c.first_name || ' ' || c.last_name as customer_name,
                   p.issue_date
            FROM prescription p
            JOIN orders o ON p.order_id = o.order_id
            JOIN customer c ON o.customer_id = c.customer_id
            WHERE p.validation_status = 'Pending'
        """

        if branch_id:
            query += " AND o.branch_id = ?"
            cursor.execute(query, (branch_id,))
        else:
            cursor.execute(query)

        return cursor.fetchall()

    def get_prescription_details(self, prescription_id):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT p.prescription_id, p.prescription_number, p.issue_date, 
                   p.validation_status, p.notes, o.order_id, c.first_name, c.last_name
            FROM prescription p
            JOIN orders o ON p.order_id = o.order_id
            JOIN customer c ON o.customer_id = c.customer_id
            WHERE p.prescription_id = ?
        """, (prescription_id,))
        return cursor.fetchone()
