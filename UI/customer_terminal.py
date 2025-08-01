# UI/customer_terminal.py

from UI.base_terminal import BaseTerminal
from Services.auth_service import AuthService
from Models.branch import Branch
from UI.menu_handlers import customer_menu

class CustomerTerminal(BaseTerminal):
    def __init__(self):
        super().__init__()
        self.auth = AuthService()
        self.branch_model = Branch()
        self.customer_id = None
        self.branch_id = None

    def run(self):
        while True:
            self.display_title("Customer Portal")
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                self.login()
            elif choice == '2':
                self.register()
            elif choice == '3':
                break
            else:
                self.notify_error("Invalid choice")

    def login(self):
        email = input("Email: ")
        phone = input("Phone: ")
        customer = self.auth.customer_model.authenticate(email, phone)
        if customer:
            self.customer_id = customer[0]
            self.notify_success(f"Welcome {customer[1]} {customer[2]}!")
            self.select_branch()
            customer_menu(self)
        else:
            self.notify_error("Login failed")

        self.customer = self.auth.customer_model.authenticate(email, phone)

        if self.customer:
            self.customer_id = self.customer[0]      # customer_id
            customer_menu(self)


    def register(self):
        self.display_section("Register")
        first = input("First name: ")
        last = input("Last name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        address = input("Address (optional): ")
        dob = input("DOB (YYYY-MM-DD, optional): ")
        if self.auth.register_customer(first, last, email, phone, address, dob):
            self.notify_success("Registration successful")
        else:
            self.notify_error("Registration failed")

    def select_branch(self):
        branches = self.branch_model.get_all_branches()
        self.display_table(branches, headers=["ID", "Name", "Address"])
        selected_id = int(input("Enter branch ID to switch: "))
        self.branch_id = selected_id
        print(f"✅ Branch changed to {selected_id}")


        

