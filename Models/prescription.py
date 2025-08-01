from Config.database_config import DatabaseConfig

class Prescription:
    def __init__(self):
        self.db = DatabaseConfig().create_connection()

    def get_by_order_id(self, order_id):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT * FROM prescription
            WHERE order_id = ?
        """, (order_id,))
        return cursor.fetchone()

    def create_prescription(self, order_id, pharmacist_id, prescription_number, issue_date, notes=None):
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO prescription (
                order_id, pharmacist_id, prescription_number,
                issue_date, validation_status, notes
            ) VALUES (?, ?, ?, ?, 'Pending', ?)
        """, (order_id, pharmacist_id, prescription_number, issue_date, notes))
        self.db.commit()
        return cursor.lastrowid

    def update_validation_status(self, prescription_id, status, notes=None):
        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE prescription
            SET validation_status = ?, validation_date = CURRENT_TIMESTAMP, notes = ?
            WHERE prescription_id = ?
        """, (status, notes, prescription_id))
        self.db.commit()
        return cursor.rowcount > 0
