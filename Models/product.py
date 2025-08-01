import sqlite3
from typing import Optional, List, Tuple, Dict


class Product:
    def __init__(self, db_path: str = 'Data/pharmacy.db'):
        self.db_path = db_path

    def connect_db(self):
        return sqlite3.connect(self.db_path)

    def get_products_by_branch(self, branch_id: int) -> List[Tuple]:
        """Get all products available at a specific branch with inventory info"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.product_id, p.product_name, p.product_description, 
                   p.unit_price, p.requires_prescription, p.product_category,
                   COALESCE(i.quantity_in_stock, 0) as branch_stock
            FROM product p
            LEFT JOIN inventory i ON p.product_id = i.product_id AND i.branch_id = ?
            ORDER BY p.product_name
        """, (branch_id,))
        
        products = cursor.fetchall()
        conn.close()
        
        return products

    def search_products_by_branch(self, branch_id: int, search_term: str) -> List[Tuple]:
        """Search products by name or description at a specific branch"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.product_id, p.product_name, p.product_description, 
                   p.unit_price, p.requires_prescription, p.product_category,
                   COALESCE(i.quantity_in_stock, 0) as branch_stock
            FROM product p
            LEFT JOIN inventory i ON p.product_id = i.product_id AND i.branch_id = ?
            WHERE p.product_name LIKE ? OR p.product_description LIKE ?
            ORDER BY p.product_name
        """, (branch_id, f'%{search_term}%', f'%{search_term}%'))
        
        products = cursor.fetchall()
        conn.close()
        
        return products

    def get_product_details(self, product_id: int, branch_id: Optional[int] = None) -> Optional[Tuple]:
        """Get detailed information about a product"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        if branch_id:
            cursor.execute("""
                SELECT p.product_id, p.product_name, p.product_description, 
                       p.unit_price, p.requires_prescription, p.product_category,
                       COALESCE(i.quantity_in_stock, 0) as branch_stock
                FROM product p
                LEFT JOIN inventory i ON p.product_id = i.product_id AND i.branch_id = ?
                WHERE p.product_id = ?
            """, (branch_id, product_id))
        else:
            cursor.execute("""
                SELECT p.product_id, p.product_name, p.product_description, 
                       p.unit_price, p.requires_prescription, p.product_category
                FROM product p
                WHERE p.product_id = ?
            """, (product_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result

    def add_product(self, product_name: str, product_description: str, 
                   product_category: str, unit_price: float, 
                   requires_prescription: bool = False) -> Tuple[bool, str]:
        """Add a new product to the system"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO product (product_name, product_description, product_category,
                                   unit_price, requires_prescription)
                VALUES (?, ?, ?, ?, ?)
            """, (product_name, product_description, product_category, 
                  unit_price, requires_prescription))
            
            conn.commit()
            product_id = cursor.lastrowid
            return True, f"Product added successfully with ID: {product_id}"
            
        except sqlite3.IntegrityError as e:
            conn.rollback()
            return False, f"Error: {str(e)}"
        except Exception as e:
            conn.rollback()
            return False, f"Unexpected error: {str(e)}"
        finally:
            conn.close()

    def update_product(self, product_id: int, **kwargs) -> Tuple[bool, str]:
        """Update product information"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query
            set_clauses = []
            values = []
            
            valid_fields = ['product_name', 'product_description', 'product_category', 
                          'unit_price', 'requires_prescription']
            
            for field, value in kwargs.items():
                if field in valid_fields:
                    set_clauses.append(f"{field} = ?")
                    values.append(value)
            
            if not set_clauses:
                return False, "No valid fields to update"
            
            values.append(product_id)
            query = f"UPDATE product SET {', '.join(set_clauses)} WHERE product_id = ?"
            
            cursor.execute(query, values)
            
            if cursor.rowcount > 0:
                conn.commit()
                return True, "Product updated successfully"
            else:
                return False, "Product not found"
                
        except Exception as e:
            conn.rollback()
            return False, f"Error updating product: {str(e)}"
        finally:
            conn.close()

    def get_products_requiring_prescription(self, branch_id: Optional[int] = None) -> List[Tuple]:
        """Get all products that require prescription"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        if branch_id:
            cursor.execute("""
                SELECT p.product_id, p.product_name, p.product_description, 
                       p.unit_price, COALESCE(i.quantity_in_stock, 0) as branch_stock
                FROM product p
                LEFT JOIN inventory i ON p.product_id = i.product_id AND i.branch_id = ?
                WHERE p.requires_prescription = 1
                ORDER BY p.product_name
            """, (branch_id,))
        else:
            cursor.execute("""
                SELECT p.product_id, p.product_name, p.product_description, p.unit_price
                FROM product p
                WHERE p.requires_prescription = 1
                ORDER BY p.product_name
            """)
        
        products = cursor.fetchall()
        conn.close()
        
        return products

    def get_product_categories(self) -> List[str]:
        """Get all unique product categories"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT product_category 
            FROM product 
            WHERE product_category IS NOT NULL 
            ORDER BY product_category
        """)
        
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return categories

    def get_products_by_category(self, category: str, branch_id: Optional[int] = None) -> List[Tuple]:
        """Get all products in a specific category"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        if branch_id:
            cursor.execute("""
                SELECT p.product_id, p.product_name, p.product_description, 
                       p.unit_price, p.requires_prescription,
                       COALESCE(i.quantity_in_stock, 0) as branch_stock
                FROM product p
                LEFT JOIN inventory i ON p.product_id = i.product_id AND i.branch_id = ?
                WHERE p.product_category = ?
                ORDER BY p.product_name
            """, (branch_id, category))
        else:
            cursor.execute("""
                SELECT p.product_id, p.product_name, p.product_description, 
                       p.unit_price, p.requires_prescription
                FROM product p
                WHERE p.product_category = ?
                ORDER BY p.product_name
            """, (category,))
        
        products = cursor.fetchall()
        conn.close()
        
        return products

    def check_stock_availability(self, product_id: int, branch_id: int, 
                               required_quantity: int) -> bool:
        """Check if sufficient stock is available at a branch"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT quantity_in_stock
            FROM inventory
            WHERE product_id = ? AND branch_id = ?
        """, (product_id, branch_id))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0] >= required_quantity
        return False

    def get_top_selling_products(self, branch_id: int, start_date: str, 
                               end_date: str, limit: int = 10) -> List[Dict]:
        """Get top selling products for a branch in a date range"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.product_id, p.product_name, p.product_category,
                   SUM(oi.quantity) as total_sold, 
                   SUM(oi.subtotal) as total_revenue
            FROM order_item oi
            JOIN orders o ON oi.order_id = o.order_id
            JOIN product p ON oi.product_id = p.product_id
            WHERE o.branch_id = ? AND DATE(o.order_date) BETWEEN ? AND ?
            GROUP BY p.product_id
            ORDER BY total_sold DESC
            LIMIT ?
        """, (branch_id, start_date, end_date, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'product_id': result[0],
            'product_name': result[1],
            'category': result[2],
            'total_sold': result[3],
            'total_revenue': result[4]
        } for result in results]

    def delete_product(self, product_id: int) -> Tuple[bool, str]:
        """Delete a product (only if not in any orders)"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        try:
            # Check if product is in any orders
            cursor.execute("""
                SELECT COUNT(*) FROM order_item WHERE product_id = ?
            """, (product_id,))
            
            if cursor.fetchone()[0] > 0:
                return False, "Cannot delete product that has been ordered"
            
            # Check if product is in any inventory
            cursor.execute("""
                SELECT COUNT(*) FROM inventory WHERE product_id = ?
            """, (product_id,))
            
            if cursor.fetchone()[0] > 0:
                return False, "Cannot delete product that exists in inventory"
            
            # Delete the product
            cursor.execute("DELETE FROM product WHERE product_id = ?", (product_id,))
            
            if cursor.rowcount > 0:
                conn.commit()
                return True, "Product deleted successfully"
            else:
                return False, "Product not found"
                
        except Exception as e:
            conn.rollback()
            return False, f"Error deleting product: {str(e)}"
        finally:
            conn.close()