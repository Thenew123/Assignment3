# main.py

from UI.customer_terminal import CustomerTerminal
from UI.staff_terminal import StaffTerminal
from UI.base_terminal import BaseTerminal

def main():
    ui = BaseTerminal()

    while True:
        ui.display_title("Long Chau Pharmacy System")
        print("1. Customer Portal")
        print("2. Staff Portal")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            customer = CustomerTerminal()
            customer.run()
        elif choice == '2':
            staff = StaffTerminal()
            staff.run()
        elif choice == '3':
            ui.notify_info("Goodbye!")
            break
        else:
            ui.notify_error("Invalid option")

if __name__ == "__main__":
    main()
