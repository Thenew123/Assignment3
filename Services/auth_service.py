# Services/auth_service.py
from Models.customer import Customer
from Models.staff import Staff

class AuthService:
    """Authentication service for customers and staff"""
    
    def __init__(self):
        self.customer_model = Customer()
        self.staff_model = Staff()
    
    def login_customer(self, email, phone):
        """Login customer with email and phone"""
        result = self.customer_model.authenticate(email, phone)
        
        if result:
            return {
                'success': True,
                'customer_id': result[0],
                'name': f"{result[1]} {result[2]}",
                'first_name': result[1],
                'last_name': result[2]
            }
        else:
            return {
                'success': False,
                'message': 'Customer not found. Please check your email and phone number.'
            }
    
    def register_customer(self, first_name, last_name, email, phone, address=None, date_of_birth=None):
        """Register new customer"""
        # Validate required fields
        if not all([first_name, last_name, email, phone]):
            return {
                'success': False,
                'message': 'Please fill in all required fields.'
            }
        
        # Create customer
        customer_id = self.customer_model.create_customer(
            first_name, last_name, email, phone, address, date_of_birth
        )
        
        if customer_id:
            return {
                'success': True,
                'customer_id': customer_id,
                'name': f"{first_name} {last_name}",
                'message': f'Registration successful! Welcome, {first_name} {last_name}'
            }
        else:
            return {
                'success': False,
                'message': 'A customer with this email already exists.'
            }
    
    def login_staff(self, email, staff_id):
        """Login staff with email and staff ID"""
        result = self.staff_model.authenticate_staff(email, staff_id)
        
        if result:
            return {
                'success': True,
                'staff_id': result["staff_id"],
                'name': f"{result['first_name']} {result['last_name']}",
                'first_name': result["first_name"],
                'last_name': result["last_name"],
                'branch_id': result["branch_id"],
                'staff_type_name': result["staff_type_name"]

            }
        else:
            return {
                'success': False,
                'message': 'Login failed. Please check your credentials.'
            }
    
    def validate_email(self, email):
        """Basic email validation"""
        return '@' in email and '.' in email.split('@')[1]
    
    def validate_phone(self, phone):
        """Basic phone validation"""
        return phone.isdigit() and len(phone) >= 10
    
    def validate_staff_id(self, staff_id):
        """Basic staff ID validation"""
        return staff_id.isdigit() and len(staff_id) > 0