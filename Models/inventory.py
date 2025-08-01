import sqlite3
from datetime import date
from typing import Optional, List, Tuple, Dict


class Inventory:
    def __init__(self, db_path: str = 'Data/pharmacy.db'):
        self.db_path = db_path

    def connect_db(self):
        return sqlite3.connect(self.db_path)

    def get_branch_inventory(self, branch_id: int) -> List[Tuple]:
        """Get all inventory items for a specific branch"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT i.inventory_id, p.product_name, p.product_category,
                   i.quantity_in_stock, p.unit_price, i.last_restocked,
                   p.requires_prescription, p.product_id
            FROM inventory i
            JOIN product p ON i.product_id = p.product_id
            WHERE i.branch_id = ?
            ORDER BY p.product_name
        """, (branch_id,))
        
        inventory = cursor.fetchall()
        conn.close()
        
        return inventory

    def get_low_stock_items(self, branch_id: int, threshold: int = 10) -> List[Tuple]:
        """Get items with stock below threshold"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT i.inventory_id, p.product_name, i.quantity_in_stock, 
                   p.unit_price, i.last_restocked
            FROM inventory i
            JOIN product p ON i.product_id = p.product_id
            WHERE i.branch_id = ? AND i.quantity_in_stock < ?
            ORDER BY i.quantity_in_stock ASC
        """, (branch_id, threshold))
        
        low_stock = cursor.fetchall()
        conn.close()
        
        return low_stock

    def search_inventory(self, branch_id: int, search_term: str) -> List[Tuple]:
        """Search inventory by product name"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT i.inventory_id, p.product_name, i.quantity_in_stock, 
                   p.unit_price, i.last_restocked
            FROM inventory i
            JOIN product p ON i.product_id = p.product_id
            WHERE i.branch_id = ? AND p.product_name LIKE ?
            ORDER BY p.product_name
        """, (branch_id, f'%{search_term}%'))
        
        results = cursor.fetchall()
        conn.close()
        
        return results

    def update_stock_quantity(self, inventory_id: int, new_quantity: int, 
                            branch_id: Optional[int] = None) -> Tuple[bool, str]:
        """Update stock quantity for an inventory item"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        try:
            if branch_id:
                cursor.execute("""
                    UPDATE inventory 
                    SET quantity_in_stock = ?, last_restocked = ?
                    WHERE inventory_id = ? AND branch_id = ?
                """, (new_quantity, date.today(), inventory_id, branch_id))
            else:
                cursor.execute("""
                    UPDATE inventory 
                    SET quantity_in_stock = ?, last_restocked = ?
                    WHERE inventory_id = ?
                """, (new_quantity, date.today(), inventory_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                return True, "Stock updated successfully"
            else:
                return False, "Inventory item not found or access denied"
                
        except Exception as e:
            conn.rollback()
            return False, f"Error updating stock: {str(e)}"
        finally:
            conn.close()

    def add_stock(self, inventory_id: int, additional_quantity: int, 
                  branch_id: Optional[int] = None) -> Tuple[bool, str]:
        """Add stock to an existing inventory item"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        try:
            if branch_id:
                cursor.execute("""
                    UPDATE inventory 
                    SET quantity_in_stock = quantity_in_stock + ?, last_restocked = ?
                    WHERE inventory_id = ? AND branch_id = ?
                """, (additional_quantity, date.today(), inventory_id, branch_id))
            else:
                cursor.execute("""
                    UPDATE inventory 
                    SET quantity_in_stock = quantity_in_stock + ?, last_restocked = ?
                    WHERE inventory_id = ?
                """, (additional_quantity, date.today(), inventory_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                return True, f"{additional_quantity} units added successfully"
            else:
                return False, "Inventory item not found or access denied"
                
        except Exception as e:
            conn.rollback()
            return False, f"Error adding stock: {str(e)}"
        finally:
            conn.close()

    def reserve_stock(self, product_id: int, branch_id: int, quantity: int) -> Tuple[bool, str]:
        """Reserve stock for an order (reduce available quantity)"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("BEGIN")
            
            # Check current available stock
            cursor.execute("""
                SELECT quantity_in_stock, inventory_id
                FROM inventory
                WHERE product_id = ? AND branch_id = ?
            """, (product_id, branch_id))
            
            result = cursor.fetchone()
            if not result:
                conn.rollback()
                return False, "Product not available at this branch"
            
            available_stock, inventory_id = result
            
            if available_stock < quantity:
                conn.rollback()
                return False, f"Insufficient stock. Available: {available_stock}, Requested: {quantity}"
            
            # Reserve stock by reducing inventory
            cursor.execute("""
                UPDATE inventory 
                SET quantity_in_stock = quantity_in_stock - ?
                WHERE inventory_id = ?
            """, (quantity, inventory_id))
            
            conn.commit()
            return True, "Stock reserved successfully"
            
        except Exception as e:
            conn.rollback()
            return False, f"Error reserving stock: {str(e)}"
        finally:
            conn.close()

    def release_stock(self, product_id: int, branch_id: int, quantity: int) -> Tuple[bool, str]:
        """Release reserved stock back to inventory"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT inventory_id
                FROM inventory
                WHERE product_id = ? AND branch_id = ?
            """, (product_id, branch_id))
            
            result = cursor.fetchone()
            if not result:
                return False, "Inventory item not found"
            
            inventory_id = result[0]
            
            cursor.execute("""
                UPDATE inventory 
                SET quantity_in_stock = quantity_in_stock + ?
                WHERE inventory_id = ?
            """, (quantity, inventory_id))
            
            conn.commit()
            return True, "Stock released successfully"
            
        except Exception as e:
            conn.rollback()
            return False, f"Error releasing stock: {str(e)}"
        finally:
            conn.close()

    def add_product_to_inventory(self, branch_id: int, product_id: int, 
                               initial_stock: int) -> Tuple[bool, str]:
        """Add a new product to branch inventory"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO inventory (branch_id, product_id, quantity_in_stock, last_restocked)
                VALUES (?, ?, ?, ?)
            """, (branch_id, product_id, initial_stock, date.today()))
            
            conn.commit()
            inventory_id = cursor.lastrowid
            return True, f"Product added to inventory with ID: {inventory_id}"
            
        except sqlite3.IntegrityError:
            conn.rollback()
            return False, "Product already exists in this branch's inventory"
        except Exception as e:
            conn.rollback()
            return False, f"Error adding product to inventory: {str(e)}"
        finally:
            conn.close()

    def remove_product_from_inventory(self, inventory_id: int, 
                                    branch_id: Optional[int] = None) -> Tuple[bool, str]:
        """Remove a product from branch inventory"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        try:
            # Check if there's any stock remaining
            if branch_id:
                cursor.execute("""
                    SELECT quantity_in_stock FROM inventory 
                    WHERE inventory_id = ? AND branch_id = ?
                """, (inventory_id, branch_id))
            else:
                cursor.execute("""
                    SELECT quantity_in_stock FROM inventory 
                    WHERE inventory_id = ?
                """, (inventory_id,))
            
            result = cursor.fetchone()
            if not result:
                return False, "Inventory item not found"
            
            if result[0] > 0:
                return False, "Cannot remove product with remaining stock"
            
            # Delete inventory item
            if branch_id:
                cursor.execute("""
                    DELETE FROM inventory 
                    WHERE inventory_id = ? AND branch_id = ?
                """, (inventory_id, branch_id))
            else:
                cursor.execute("""
                    DELETE FROM inventory 
                    WHERE inventory_id = ?
                """, (inventory_id,))
            
            if cursor.rowcount > 0:
                conn.commit()
                return True, "Product removed from inventory"
            else:
                return False, "Inventory item not found or access denied"
                
        except Exception as e:
            conn.rollback()
            return False, f"Error removing product from inventory: {str(e)}"
        finally:
            conn.close()

    def get_inventory_value(self, branch_id: int) -> Dict:
        """Calculate total inventory value for a branch"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) as total_products, 
                   SUM(quantity_in_stock) as total_stock,
                   SUM(quantity_in_stock * p.unit_price) as inventory_value
            FROM inventory i
            JOIN product p ON i.product_id = p.product_id
            WHERE i.branch_id = ?
        """, (branch_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            'total_products': result[0] if result[0] else 0,
            'total_stock': result[1] if result[1] else 0,
            'inventory_value': result[2] if result[2] else 0.0
        }

    def get_products_not_in_inventory(self, branch_id: int) -> List[Tuple]:
        """Get products that are not in this branch's inventory"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.product_id, p.product_name, p.unit_price, p.product_category
            FROM product p
            WHERE p.product_id NOT IN (
                SELECT product_id FROM inventory WHERE branch_id = ?
            )
            ORDER BY p.product_name
        """, (branch_id,))
        
        available_products = cursor.fetchall()
        conn.close()
        
        return available_products

    def get_inventory_movement_history(self, branch_id: int, days: int = 30) -> List[Dict]:
        """Get inventory movement history for reporting"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        # This would require additional tables to track inventory movements
        # For now, we'll return restock history
        cursor.execute("""
            SELECT p.product_name, i.quantity_in_stock, i.last_restocked
            FROM inventory i
            JOIN product p ON i.product_id = p.product_id
            WHERE i.branch_id = ? AND i.last_restocked >= DATE('now', '-{} days')
            ORDER BY i.last_restocked DESC
        """.format(days), (branch_id,))
        
        history = cursor.fetchall()
        conn.close()
        
        return [{
            'product_name': item[0],
            'current_stock': item[1],
            'last_restocked': item[2]
        } for item in history]

    def check_stock_availability(self, product_id: int, branch_id: int, 
                               required_quantity: int) -> Tuple[bool, int]:
        """Check if sufficient stock is available"""
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
            available_stock = result[0]
            return available_stock >= required_quantity, available_stock
        return False, 0