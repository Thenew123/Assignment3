# UI/menu_handlers.py

from Services.order_service import OrderService
from Services.prescription_service import PrescriptionService
from Services.inventory_service import InventoryService
from Services.report_service import ReportService
from Services.staff_service import StaffService
from Models.customer import Customer
from Models.product import Product
from Services.payment_service import PaymentService
# ----- CUSTOMER MENU -----
def customer_menu(term):
    order_service = OrderService()
    product_model = Product()
    customer_model = Customer()
    payment_service = PaymentService()

    while True:
        term.display_section("Customer Menu")
        print("1. Browse Products")
        print("2. Search Products")
        print("3. View Shopping Cart")
        print("4. Place Order")
        print("5. View My Orders")
        print("6. Upload Prescription")
        print("7. Change Branch")
        print("8. Logout")
        choice = input("Choose an option: ")

        if choice == '1':
            products = product_model.get_products_by_branch(term.branch_id)
            term.display_table(products, headers=["ID", "Name","Description", "Price","Prescription Required","Category", "Stock"])
            add_choice = input("Would you like to add a product to your cart? (y/n): ").lower()
            if add_choice == "y":
                try:
                    product_id = int(input("Enter Product ID: "))
                    quantity = int(input("Enter Quantity: "))
                    result = order_service.add_to_cart(term.customer_id, product_id, quantity)

                    if result["success"]:
                        term.notify_success(result["message"])
                    else:
                        term.notify_error(result["message"])
                except ValueError:
                    term.notify_error("Invalid input. Please enter numeric values.")

        elif choice == '2':
            keyword = input("Search keyword: ")
            results = product_model.search_products_by_branch(term.branch_id, keyword)
            term.display_table(results, headers=["ID", "Name","Description", "Price","Prescription Required","Category", "Stock"])
        elif choice == '3':
            items = order_service.get_cart_items(term.customer_id)
            term.display_table(items, headers=["Product ID", "Name", "Qty", "Unit Price", "Subtotal"])
        elif choice == "4":
            # Checkout order
            order_result = order_service.checkout(term.customer_id, term.branch_id)
            if not order_result["success"]:
                term.notify_error(order_result["message"])
                return
            
            order_id = order_result["order_id"]
            amount = order_result["total_amount"]
            term.notify_success(f"Order #{order_id} created. Total: ${amount:.2f}")
            
            # Display payment methods
            methods = payment_service.get_methods()
            if not methods:
                term.notify_error("No payment methods available.")
                return

            term.display_table(methods, ["ID", "Method"])
            
            try:
                method_id = int(input("Select Payment Method ID: "))
                valid_ids = [m[0] for m in methods]
                if method_id not in valid_ids:
                    term.notify_error("Invalid payment method selected.")
                    return

                reference = input("Enter Transaction Reference (optional): ").strip()
                payment_service.process_payment(order_id, method_id, amount, reference)
                term.notify_success("Payment completed successfully.")

            except ValueError:
                term.notify_error("Invalid input for payment method.")

        elif choice == '5':
            orders = customer_model.get_customer_orders(term.customer_id)
            term.display_table(orders, headers=["Order ID", "Date", "Amount", "Status"])
        elif choice == '6':
            input("Simulating prescription upload (Press Enter)...")
            term.notify_success("Prescription uploaded.")
        elif choice == '7':
            term.select_branch()
        elif choice == '8':
            break
        else:
            term.notify_error("Invalid option")

# ----- PHARMACIST MENU -----
def pharmacist_menu(term):
    prescriptions = PrescriptionService()

    while True:
        term.display_section("PHARMACIST DASHBOARD")
        print("1. View Prescriptions for Validation")
        print("2. Validate Prescription")
        print("3. Search Prescriptions")
        print("4. View My Validation History")
        print("5. Logout")

        choice = input("Choose an option: ")

        if choice == '1':
            pending = prescriptions.get_pending_prescriptions(term.branch_id)
            term.display_table(pending, headers=["ID", "Number", "Order", "Customer", "Issue Date"])
        elif choice == '2':
            pid = input("Enter Prescription ID to validate: ")
            prescriptions.validate_prescription(pid, term.staff_id)
            term.notify_success("Prescription validated.")
        elif choice == '3':
            keyword = input("Enter prescription number or customer: ")
            input("Search feature stubbed.")  # Replace with real search
        elif choice == '4':
            input("Validation history feature stubbed.")
        elif choice == '5':
            break
        else:
            term.notify_error("Invalid option")


# ----- BRANCH MANAGER MENU -----
def manager_menu(term):
    inventory = InventoryService()
    reports = ReportService()
    staff = StaffService()

    while True:
        term.display_section("BRANCH MANAGER DASHBOARD")
        print("1. View Staff")
        print("2. Manage Staff")
        print("3. View Inventory")
        print("4. Manage Inventory")
        print("5. Create Reports")
        print("6. View Reports")
        print("7. Branch Statistics")
        print("8. Logout")

        choice = input("Choose an option: ")

        if choice == '1':
            staff_list = staff.get_staff_by_branch(term.branch_id)
            term.display_table(staff_list, headers=["ID", "Name", "Role", "Email"])
        elif choice == '2':
            input("Staff management feature stubbed.")
        elif choice == '3':
            items = inventory.get_inventory_by_branch(term.branch_id)
            term.display_table(items, headers=["ID", "Product", "Qty", "Restocked"])
        elif choice == '4':
            input("Inventory management stub.")
        elif choice == '5':
            start = input("Start date: ")
            end = input("End date: ")
            title = input("Title: ")
            stats = reports.generate_sales_summary(term.branch_id, start, end)
            summary = f"Orders: {stats[0]}, Revenue: ${stats[1]}, Avg: ${stats[2]}"
            reports.create_report(term.staff_id, term.branch_id, "Sales", title, start, end, summary)
            term.notify_success("Report created.")
        elif choice == '6':
            data = reports.get_reports_by_branch(term.branch_id)
            term.display_table(data, headers=["ID", "Title", "Type", "Start", "End", "Date"])
        elif choice == '7':
            stat = reports.generate_sales_summary(term.branch_id, "2000-01-01", "2100-01-01")
            print(f"\nTotal Orders: {stat[0]}\nRevenue: ${stat[1]}\nAvg Order: ${stat[2]}")
        elif choice == '8':
            break
        else:
            term.notify_error("Invalid option")
