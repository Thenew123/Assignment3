from Config.database_config import DatabaseConfig

class Branch:
    def __init__(self):
        self.db = DatabaseConfig().create_connection()

    def get_all_branches(self):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT branch_id, branch_name, branch_address, branch_phone
            FROM branch
            ORDER BY branch_name
        """)
        return cursor.fetchall()

    def get_branch_by_id(self, branch_id):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT branch_id, branch_name, branch_address, branch_phone
            FROM branch
            WHERE branch_id = ?
        """, (branch_id,))
        return cursor.fetchone()
