import sqlite3
from datetime import datetime, date
from typing import Optional, List, Tuple, Dict, Any


class Staff:
    def __init__(self, db_path: str = 'Data/pharmacy.db'):
        self.db_path = db_path

    def connect_db(self):
        return sqlite3.connect(self.db_path)

    def authenticate_staff(self, email: str, staff_id: str) -> Optional[Dict[str,Any]]:
        """Authenticate staff member and return their details"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.staff_id, s.first_name, s.last_name, s.branch_id, st.staff_type_name
            FROM staff s
            JOIN staff_type st ON s.staff_type = st.staff_type_id
            WHERE s.email = ? AND s.staff_id = ?
        """, (email, staff_id))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
            "staff_id": result[0],
            "first_name": result[1],
            "last_name": result[2],
            "branch_id": result[3],
            "staff_type_name": result[4]
            }
        return None
        

    def get_staff_by_branch(self, branch_id: int) -> List[Tuple]:
        """Get all staff members for a specific branch"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.staff_id, s.first_name, s.last_name, st.staff_type_name,
                   s.email, s.phone, s.hire_date, s.salary
            FROM staff s
            JOIN staff_type st ON s.staff_type = st.staff_type_id
            WHERE s.branch_id = ?
            ORDER BY st.staff_type_name, s.last_name
        """, (branch_id,))
        
        staff_list = cursor.fetchall()
        conn.close()
        
        return staff_list

    def get_staff_details(self, staff_id: int) -> Optional[Tuple]:
        """Get detailed information about a staff member"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.staff_id, s.first_name, s.last_name, st.staff_type,
                   s.email, s.phone, s.hire_date, s.salary, s.branch_id,
                   b.branch_name
            FROM staff s
            JOIN staff_type st ON s.staff_type = st.staff_type_id
            JOIN branch b ON s.branch_id = b.branch_id
            WHERE s.staff_id = ?
        """, (staff_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result

    def add_staff_member(self, first_name: str, last_name: str, staff_type: int, 
                        branch_id: int, email: str, phone: str, salary: float) -> Tuple[bool, str]:
        """Add a new staff member"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO staff (first_name, last_name, staff_type, branch_id, 
                                 email, phone, hire_date, salary)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (first_name, last_name, staff_type, branch_id, email, phone, 
                  date.today(), salary))
            
            conn.commit()
            staff_id = cursor.lastrowid
            return True, f"Staff member added successfully with ID: {staff_id}"
            
        except sqlite3.IntegrityError as e:
            conn.rollback()
            return False, f"Error: {str(e)}"
        except Exception as e:
            conn.rollback()
            return False, f"Unexpected error: {str(e)}"
        finally:
            conn.close()

    def update_staff_member(self, staff_id: int, **kwargs) -> Tuple[bool, str]:
        """Update staff member information"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query
            set_clauses = []
            values = []
            
            for field, value in kwargs.items():
                if field in ['first_name', 'last_name', 'email', 'phone', 'salary']:
                    set_clauses.append(f"{field} = ?")
                    values.append(value)
            
            if not set_clauses:
                return False, "No valid fields to update"
            
            values.append(staff_id)
            query = f"UPDATE staff SET {', '.join(set_clauses)} WHERE staff_id = ?"
            
            cursor.execute(query, values)
            
            if cursor.rowcount > 0:
                conn.commit()
                return True, "Staff member updated successfully"
            else:
                return False, "Staff member not found"
                
        except Exception as e:
            conn.rollback()
            return False, f"Error updating staff: {str(e)}"
        finally:
            conn.close()

    def get_staff_types(self) -> List[Tuple]:
        """Get all available staff types"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT staff_type_id, staff_type_name FROM staff_type")
        staff_types = cursor.fetchall()
        conn.close()
        
        return staff_types

    def get_pharmacists(self, branch_id: Optional[int] = None) -> List[Tuple]:
        """Get all pharmacists, optionally filtered by branch"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        if branch_id:
            cursor.execute("""
                SELECT s.staff_id, s.first_name, s.last_name, s.email
                FROM staff s
                JOIN staff_type st ON s.staff_type = st.staff_type_id
                WHERE st.staff_type_name = 'Pharmacist' AND s.branch_id = ?
            """, (branch_id,))
        else:
            cursor.execute("""
                SELECT s.staff_id, s.first_name, s.last_name, s.email, s.branch_id
                FROM staff s
                JOIN staff_type st ON s.staff_type = st.staff_type_id
                WHERE st.staff_type_name = 'Pharmacist'
            """)
        
        pharmacists = cursor.fetchall()
        conn.close()
        
        return pharmacists

    def get_staff_performance(self, branch_id: int, start_date: date, end_date: date) -> List[Dict]:
        """Get staff performance data for reporting"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.staff_id, s.first_name, s.last_name, st.staff_type_name,
                   COUNT(p.prescription_id) as prescriptions_processed
            FROM staff s
            JOIN staff_type st ON s.staff_type = st.staff_type_id
            LEFT JOIN prescription p ON s.staff_id = p.pharmacist_id 
                AND DATE(p.validation_date) BETWEEN ? AND ?
            WHERE s.branch_id = ?
            GROUP BY s.staff_id
            ORDER BY prescriptions_processed DESC
        """, (start_date, end_date, branch_id))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'staff_id': result[0],
            'name': f"{result[1]} {result[2]}",
            'type': result[3],
            'prescriptions_processed': result[4]
        } for result in results]

    def has_permission(self, staff_id: int, permission: str) -> bool:
        """Check if staff member has specific permission based on their role"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT st.staff_type_name
            FROM staff s
            JOIN staff_type st ON s.staff_type = st.staff_type_id
            WHERE s.staff_id = ?
        """, (staff_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return False
        
        staff_type = result[0]
        
        # Define permissions by role
        permissions = {
            'Pharmacist': ['validate_prescription', 'view_prescriptions', 'search_prescriptions'],
            'BranchManager': ['manage_staff', 'manage_inventory', 'create_reports', 
                            'view_reports', 'branch_statistics', 'validate_prescription'],
            'Cashier': ['view_orders', 'update_order_status', 'process_payments']
        }
        
        return permission in permissions.get(staff_type, [])