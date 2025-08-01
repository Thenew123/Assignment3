from Config.database_config import DatabaseConfig
import sqlite3

class OrderService:
    def __init__(self):
        self.db = DatabaseConfig().create_connection()


    def add_to_cart(self, customer_id, product_id, quantity):
        cursor = self.db.cursor()

        # Check if product exists and stock is enough
        cursor.execute("SELECT quantity_in_stock FROM inventory WHERE product_id = ?", (product_id,))
        row = cursor.fetchone()
        if not row:
            return {"success": False, "message": "Product does not exist."}
        
        stock = row[0]
        if quantity > stock:
            return {"success": False, "message": f"Only {stock} items in stock."}

        # Check if already in cart
        cursor.execute("""
            SELECT quantity FROM cart WHERE customer_id = ? AND product_id = ?
        """, (customer_id, product_id))
        existing = cursor.fetchone()

        if existing:
            # Update quantity
            new_quantity = existing[0] + quantity
            cursor.execute("""
                UPDATE cart SET quantity = ? WHERE customer_id = ? AND product_id = ?
            """, (new_quantity, customer_id, product_id))
        else:
            # Insert new item
            cursor.execute("""
                INSERT INTO cart (customer_id, product_id, quantity)
                VALUES (?, ?, ?)
            """, (customer_id, product_id, quantity))

        self.db.commit()
        return {"success": True, "message": "Item added to cart successfully."}

    
    def get_cart_items(self, customer_id):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT c.product_id, p.product_name, c.quantity, p.unit_price,
                   c.quantity * p.unit_price as subtotal
            FROM cart c
            JOIN product p ON c.product_id = p.product_id
            WHERE c.customer_id = ?
        """, (customer_id,))
        return cursor.fetchall()

    def clear_cart(self, customer_id):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM cart WHERE customer_id = ?", (customer_id,))
        self.db.commit()

    def checkout(self, customer_id, branch_id):
        items = self.get_cart_items(customer_id)
        if not items:
            return {
                "success": False,
                "message": "Cart is empty"
            }

        total = sum([item[4] for item in items])
        order_cursor = self.db.cursor()
        order_cursor.execute("""
            INSERT INTO orders (customer_id, branch_id, total_amount)
            VALUES (?, ?, ?)
        """, (customer_id, branch_id, total))
        order_id = order_cursor.lastrowid

        for item in items:
            product_id, _, quantity, unit_price, subtotal = item
            order_cursor.execute("""
                INSERT INTO order_item (order_id, product_id, quantity, unit_price, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """, (order_id, product_id, quantity, unit_price, subtotal))

        self.clear_cart(customer_id)
        self.db.commit()

        return {
            "success": True,
            "order_id": order_id,
            "total_amount": total
        }

