from Services.auth_service import AuthService
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
