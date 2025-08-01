# UI/staff_terminal.py

from UI.base_terminal import BaseTerminal
from Services.auth_service import AuthService
from UI.menu_handlers import pharmacist_menu, manager_menu
from Config.app_config import ROLE_PHARMACIST, ROLE_MANAGER

class StaffTerminal(BaseTerminal):
    def __init__(self):
        super().__init__()
        self.auth = AuthService()
        self.staff_id = None
        self.staff_type = None
        self.branch_id = None

    def run(self):
        self.display_title("Staff Login")
        email = input("Email: ")
        staff_id = input("Staff ID: ")
        staff = self.auth.login_staff(email, staff_id)

        if staff["success"]:
            self.staff_id = staff["staff_id"]
            self.staff_type = staff["staff_type_name"]
            self.branch_id = staff["branch_id"]
            self.notify_success(f"Welcome, {staff['first_name']} ({self.staff_type})")

            if self.staff_type == ROLE_PHARMACIST:
                pharmacist_menu(self)
            elif self.staff_type == ROLE_MANAGER:
                manager_menu(self)
            else:
                self.notify_error("Unauthorized staff type")
        else:
            self.notify_error(staff["message"])
