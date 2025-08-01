from Config.database_config import DatabaseConfig

class Report:
    def __init__(self):
        self.db = DatabaseConfig().create_connection()

    def get_reports_by_manager(self, manager_id):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT report_id, report_title, report_type,
                   report_period_start, report_period_end, generated_date
            FROM report
            WHERE branch_manager_id = ?
            ORDER BY generated_date DESC
        """, (manager_id,))
        return cursor.fetchall()

    def get_report(self, report_id):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT * FROM report
            WHERE report_id = ?
        """, (report_id,))
        return cursor.fetchone()
