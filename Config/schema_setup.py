# Config/schema_setup.py
from .database_config import DatabaseConfig

class SchemaSetup:
    """Database schema creation and management"""
    
    def __init__(self):
        self.db_config = DatabaseConfig()
    
    def create_all_tables(self):
        """Create all database tables"""
        conn = self.db_config.create_connection()
        cursor = conn.cursor()
        
        try:
            # Create all tables
            self._create_branch_table(cursor)
            self._create_staff_type_table(cursor)
            self._create_staff_table(cursor)
            self._create_customer_table(cursor)
            self._create_product_table(cursor)
            self._create_inventory_table(cursor)
            self._create_orders_table(cursor)
            self._create_order_item_table(cursor)
            self._create_cart_table(cursor)
            self._create_payment_method_table(cursor)
            self._create_payment_table(cursor)
            self._create_payment_details_table(cursor)
            self._create_prescription_table(cursor)
            self._create_notification_table(cursor)
            self._create_report_table(cursor)
            
            # Create indexes
            self._create_indexes(cursor)
            
            conn.commit()
            print("Pharmacy database schema created successfully!")
            
        except Exception as e:
            conn.rollback()
            print(f"Error creating schema: {e}")
            raise
        finally:
            conn.close()
    
    def _create_branch_table(self, cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS branch (
            branch_id INTEGER PRIMARY KEY AUTOINCREMENT,
            branch_name TEXT NOT NULL,
            branch_address TEXT NOT NULL,
            branch_phone TEXT
        )""")
    
    def _create_staff_type_table(self, cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS staff_type (
            staff_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_type_name TEXT NOT NULL UNIQUE
        )""")
    
    def _create_staff_table(self, cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS staff (
            staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            staff_type INTEGER NOT NULL,
            branch_id INTEGER NOT NULL,
            email TEXT,
            phone TEXT,
            hire_date DATE,
            salary REAL,
            FOREIGN KEY (branch_id) REFERENCES branch(branch_id),
            FOREIGN KEY (staff_type) REFERENCES staff_type(staff_type_id)
        )""")
    
    def _create_customer_table(self, cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS customer (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            address TEXT,
            date_of_birth DATE
        )""")
    
    def _create_product_table(self, cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS product (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            product_description TEXT,
            product_category TEXT,
            unit_price REAL NOT NULL,
            requires_prescription BOOLEAN DEFAULT 0
        )""")
    
    def _create_inventory_table(self, cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS inventory (
            inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
            branch_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity_in_stock INTEGER NOT NULL DEFAULT 0,
            last_restocked DATE,
            FOREIGN KEY (branch_id) REFERENCES branch(branch_id),
            FOREIGN KEY (product_id) REFERENCES product(product_id),
            UNIQUE(branch_id, product_id)
        )""")
    
    def _create_orders_table(self, cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            branch_id INTEGER NOT NULL,
            order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            order_status TEXT DEFAULT 'Pending' CHECK (order_status IN ('Pending', 'Processing', 'Ready', 'Completed', 'Cancelled')),
            total_amount REAL DEFAULT 0.0,
            FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
            FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
        )""")
    
    def _create_order_item_table(self, cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS order_item (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES product(product_id)
        )""")
    
    def _create_cart_table(self, cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS cart (
            cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            reserved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
            FOREIGN KEY (product_id) REFERENCES product(product_id),
            UNIQUE(customer_id, product_id)
        )""")
    
    def _create_payment_method_table(self, cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS payment_method (
            payment_method_id INTEGER PRIMARY KEY AUTOINCREMENT,
            method_type TEXT NOT NULL
        )""")
    
    def _create_payment_table(self, cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS payment (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL UNIQUE,
            payment_method_id INTEGER NOT NULL,
            payment_amount REAL NOT NULL,
            payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            payment_status TEXT DEFAULT 'Pending' CHECK (payment_status IN ('Pending', 'Completed', 'Failed', 'Refunded')),
            transaction_reference TEXT,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (payment_method_id) REFERENCES payment_method(payment_method_id)
        )""")
    
    def _create_payment_details_table(self, cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS payment_details (
            detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_method_id INTEGER NOT NULL,
            card_number TEXT NOT NULL,
            expiration_date DATE,
            cvv INTEGER NOT NULL,
            FOREIGN KEY (payment_method_id) REFERENCES payment_method(payment_method_id)
        )""")
    
    def _create_prescription_table(self, cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS prescription (
            prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            pharmacist_id INTEGER NOT NULL,
            prescription_number TEXT UNIQUE NOT NULL,
            issue_date DATE NOT NULL,
            validation_status TEXT DEFAULT 'Pending' CHECK (validation_status IN ('Pending', 'Validated', 'Rejected')),
            validation_date DATETIME,
            notes TEXT,
            prescription_file BLOB,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (pharmacist_id) REFERENCES staff(staff_id)
        )""")
    
    def _create_notification_table(self, cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS notification (
            notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_id INTEGER,
            notification_type TEXT NOT NULL CHECK (notification_type IN ('Order_Confirmation', 'Status_Update', 'Ready_For_Pickup', 'Prescription_Ready', 'General')),
            message TEXT NOT NULL,
            sent_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_read BOOLEAN DEFAULT 0,
            delivery_method TEXT DEFAULT 'Email' CHECK (delivery_method IN ('Email', 'SMS', 'Push', 'In_App')),
            FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        )""")
    
    def _create_report_table(self, cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS report (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            branch_manager_id INTEGER NOT NULL,
            branch_id INTEGER NOT NULL,
            report_type TEXT NOT NULL CHECK (report_type IN ('Sales', 'Inventory', 'Staff_Performance', 'Customer_Satisfaction', 'Financial')),
            report_title TEXT NOT NULL,
            report_period_start DATE,
            report_period_end DATE,
            generated_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            report_data TEXT,
            FOREIGN KEY (branch_manager_id) REFERENCES staff(staff_id),
            FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
        )""")
    
    def _create_indexes(self, cursor):
        """Create database indexes for better performance"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_staff_branch ON staff(branch_id)",
            "CREATE INDEX IF NOT EXISTS idx_staff_type ON staff(staff_type)",
            "CREATE INDEX IF NOT EXISTS idx_order_customer ON orders(customer_id)",
            "CREATE INDEX IF NOT EXISTS idx_order_date ON orders(order_date)",
            "CREATE INDEX IF NOT EXISTS idx_inventory_branch ON inventory(branch_id)",
            "CREATE INDEX IF NOT EXISTS idx_prescription_pharmacist ON prescription(pharmacist_id)",
            "CREATE INDEX IF NOT EXISTS idx_notification_customer ON notification(customer_id)"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)

    