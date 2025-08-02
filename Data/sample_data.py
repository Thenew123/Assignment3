# Data/sample_data.py

from Config.database_config import DatabaseConfig
from datetime import date

def insert_sample_data():
    db = DatabaseConfig().create_connection()
    cursor = db.cursor()

    # Insert Branches
    cursor.execute("DELETE FROM branch")
    cursor.executemany("""
        INSERT INTO branch (branch_name, branch_address, branch_phone)
        VALUES (?, ?, ?)
    """, [
        ("District 1", "123 Nguyen Trai, D1", "0909123456"),
        ("District 3", "456 Cach Mang Thang 8, D3", "0909876543"),
    ])

    # Insert Customers
    cursor.execute("DELETE FROM customer")
    cursor.execute("""
    INSERT INTO customer (first_name, last_name, email, phone, address, date_of_birth)
    VALUES (?, ?, ?, ?, ?, ?)
""", ("Alice", "Pham", "alice@gmail.com", "0909111222", "789 Dien Bien Phu", "1995-08-15"))

    # Insert Staff Types
    cursor.execute("DELETE FROM staff_type")
    cursor.executemany("""
        INSERT INTO staff_type (staff_type_name)
        VALUES (?)
    """, [
        ("Pharmacist",),
        ("BranchManager",),
    ])


    # Insert Staff (Pharmacist + Branch Manager)
    cursor.execute("DELETE FROM staff")
    cursor.executemany("""
        INSERT INTO staff (first_name, last_name, staff_type, branch_id, email, phone, hire_date, salary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        ("Linh", "Nguyen", 1, 1, "linh.pharm@longchau.vn", "0909000001", "2023-01-01", 15000000),
        ("Khoa", "Tran", 2, 1, "khoa.manager@longchau.vn", "0909000002", "2023-01-01", 18000000),
    ])


    # Insert Products
    cursor.execute("DELETE FROM product")
    cursor.executemany("""
        INSERT INTO product (product_name, product_description, product_category, unit_price, requires_prescription)
        VALUES (?, ?, ?, ?, ?)
    """, [
        ("Panadol Extra","Help to relief pain" , "Pain relief", 18000, 1),
        ("Aspirin 500mg","Anti inflammatory", "Anti-inflammatory", 15000, 0),
        ("Vitamin C","Support Immune", "Immune support", 12000, 1),
    ])

    # Insert Payment Methods
    cursor.execute("DELETE FROM payment_method")
    cursor.executemany("""
        INSERT INTO payment_method (method_type)
        VALUES (?)
    """, [
        ("Cash",),
        ("Card",),
        ("EWallet",),
    ])

    # Insert Inventory for branch 1
    cursor.execute("DELETE FROM inventory")
    cursor.executemany("""
        INSERT INTO inventory (branch_id, product_id, quantity_in_stock, last_restocked)
        VALUES (?, ?, ?, ?)
    """, [
        (1, 1, 100, date.today()),
        (1, 2, 80, date.today()),
        (1, 3, 150, date.today()),
    ])


    db.commit()
    print("✅ Sample data inserted.")
