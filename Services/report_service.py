from Config.database_config import DatabaseConfig
from datetime import datetime

class ReportService:
    def __init__(self):
        self.db = DatabaseConfig().create_connection()

    def create_report(self, manager_id, branch_id, report_type, title, start_date, end_date, report_data):
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO report (
                branch_manager_id, branch_id, report_type,
                report_title, report_period_start, report_period_end,
                generated_date, report_data
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            manager_id, branch_id, report_type, title,
            start_date, end_date, datetime.now(), report_data
        ))
        self.db.commit()
        return cursor.lastrowid

    def get_reports_by_branch(self, branch_id):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT report_id, report_title, report_type, report_period_start,
                   report_period_end, generated_date
            FROM report
            WHERE branch_id = ?
            ORDER BY generated_date DESC
        """, (branch_id,))
        return cursor.fetchall()

    def get_report_details(self, report_id):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT report_title, report_type, report_period_start, report_period_end, report_data
            FROM report
            WHERE report_id = ?
        """, (report_id,))
        return cursor.fetchone()

    def generate_sales_summary(self, branch_id, start_date, end_date):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT COUNT(*) AS total_orders,
                   SUM(total_amount) AS total_revenue,
                   AVG(total_amount) AS average_order_value
            FROM orders
            WHERE branch_id = ? AND order_date BETWEEN ? AND ?
        """, (branch_id, start_date, end_date))
        return cursor.fetchone()
