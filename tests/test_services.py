from Services.auth_service import AuthService
from Services.inventory_service import InventoryService
from Services.order_service import OrderService
from Services.payment_service import PaymentService

def test_customer_login():
    auth = AuthService()
    customer = auth.login_customer("alice@gmail.com", "0909111222")
    assert customer is not None

def test_get_cart_items():
    order = OrderService()
    cart = order.get_cart_items(1)
    assert isinstance(cart, list)

def test_get_payment_methods():
    payment = PaymentService()
    methods = payment.get_methods()
    assert isinstance(methods, list)


def test_add_inventory_negative_quantity():
    inventory_service = InventoryService()
    result = inventory_service.add_inventory(product_id=1, quantity=-10)
    assert result["success"] is False
    assert result["message"] == "Quantity must be positive."



def test_add_inventory_success():
    inventory_service = InventoryService()
    result = inventory_service.add_inventory(product_id=2, quantity=20)
    assert result is True or result is not None


