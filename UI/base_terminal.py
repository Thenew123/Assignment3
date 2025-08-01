# UI/base_terminal.py
import os
from Config.database_config import DatabaseConfig
from Config.app_config import DISPLAY_WIDTH

class BaseTerminal:
    """Base class for terminal interfaces"""
    
    def __init__(self):
        self.db_config = DatabaseConfig()
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self, title="LONG CHAU PHARMACY"):
        """Display terminal header"""
        print("=" * DISPLAY_WIDTH)
        print(title.center(DISPLAY_WIDTH))
        print("=" * DISPLAY_WIDTH)

    
    def get_user_input(self, prompt, required=True):
        """Get user input with validation"""
        while True:
            value = input(prompt).strip()
            if not required or value:
                return value
            print("This field is required. Please try again.")
    
    def get_numeric_input(self, prompt, min_value=None, max_value=None):
        """Get numeric input with validation"""
        while True:
            try:
                value = float(input(prompt))
                if min_value is not None and value < min_value:
                    print(f"Value must be at least {min_value}")
                    continue
                if max_value is not None and value > max_value:
                    print(f"Value must be at most {max_value}")
                    continue
                return value
            except ValueError:
                print("Please enter a valid number.")
    
    def get_integer_input(self, prompt, min_value=None, max_value=None):
        """Get integer input with validation"""
        value = self.get_numeric_input(prompt, min_value, max_value)
        return int(value)
    
    def confirm_action(self, message):
        """Get user confirmation"""
        response = input(f"{message} (y/n): ").lower().strip()
        return response == 'y'
    
    def display_menu(self, title, options):
        """Display menu options"""
        print(f"{title}")
        print("-" * len(title))
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print()
    
    def get_menu_choice(self, max_options):
        """Get menu choice with validation"""
        while True:
            try:
                choice = int(input(f"Enter your choice (1-{max_options}): "))
                if 1 <= choice <= max_options:
                    return choice
                print(f"Please enter a number between 1 and {max_options}")
            except ValueError:
                print("Please enter a valid number.")
    
    def pause(self, message="Press Enter to continue..."):
        """Pause execution"""
        input(message)
    
    def display_table(self, headers, rows, column_widths=None):
        """Display data in table format"""
        if not column_widths:
            column_widths = [15] * len(headers)
        
        # Print headers
        header_row = ""
        for i, header in enumerate(headers):
            header_row += f"{header[:column_widths[i]-1]:<{column_widths[i]}}"
        print(header_row)
        print("-" * sum(column_widths))
        
        # Print rows
        for row in rows:
            row_str = ""
            for i, cell in enumerate(row):
                cell_str = str(cell)[:column_widths[i]-1]
                row_str += f"{cell_str:<{column_widths[i]}}"
            print(row_str)
    
    def display_error(self, message):
        """Display error message"""
        print(f"❌ Error: {message}")
    
    def display_success(self, message):
        """Display success message"""
        print(f"✅ {message}")
    
    def display_warning(self, message):
        """Display warning message"""
        print(f"⚠️  {message}")
    
    def display_title(self, title):
        print("=" * 60)
        print(title.center(60))
        print("=" * 60)

    def display_section(self, label):
        print(f"\n-- {label} --")

    def display_table(self, rows, headers=None):
        if not rows:
            print("No data available.")
            return

        if headers:
            print(" | ".join(headers))
            print("-" * 60)

        for row in rows:
            print(" | ".join(str(cell) for cell in row))

    def notify_success(self, message):
        print(f"[✔] {message}")

    def notify_error(self, message):
        print(f"[✘] {message}")

    def notify_info(self, message):
        print(f"[i] {message}")

    def connect_db(self):
        """Create database connection"""
        return self.db_config.create_connection()