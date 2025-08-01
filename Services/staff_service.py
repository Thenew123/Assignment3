# Services/staff_service.py

from Config.database_config import DatabaseConfig

class StaffService:
    def __init__(self):
        self.db = DatabaseConfig().create_connection()

    def get_staff_by_branch(self, branch_id):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT staff_id, first_name || ' ' || last_name AS full_name, staff_type, email
            FROM staff
            WHERE branch_id = ?
        """, (branch_id,))
        return cursor.fetchall()

    def create_staff(self, first_name, last_name, staff_type, email, phone, hire_date, salary, branch_id):
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO staff (
                first_name, last_name, staff_type, email, phone, hire_date, salary, branch_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, staff_type, email, phone, hire_date, salary, branch_id))
        self.db.commit()
        return cursor.lastrowid

    def update_staff_role(self, staff_id, new_role):
        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE staff SET role = ? WHERE staff_id = ?
        """, (new_role, staff_id))
        self.db.commit()
        return cursor.rowcount > 0

    def delete_staff(self, staff_id):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM staff WHERE staff_id = ?", (staff_id,))
        self.db.commit()
        return cursor.rowcount > 0
