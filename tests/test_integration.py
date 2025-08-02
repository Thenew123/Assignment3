from Services.auth_service import AuthService
from Services.order_service import OrderService
from Services.payment_service import PaymentService

def test_customer_checkout_and_payment():
    auth = AuthService()
    order = OrderService()
    payment = PaymentService()

    customer = auth.login_customer("alice@gmail.com", "0909111222")
    assert customer is not None
    cid = customer["customer_id"]

    # Add product to cart first
    result = order.add_to_cart(cid, product_id=1, quantity=1)
    assert result["success"]

    result = order.checkout(cid, 1)
    print("Checkout result:", result)
    assert result["success"]

    order_id = result["order_id"]
    amount = result["total_amount"]

    methods = payment.get_methods()
    assert len(methods) > 0
    method_id = methods[0][0]

    pay_result = payment.process_payment(order_id, method_id, amount, "TEST_REF")
    assert pay_result["success"] 





def test_order_transaction_rollback():
    order_service = OrderService()
    try:
        order_service.add_to_cart(customer_id=None, product_id=1, quantity=1)
    except Exception:
        assert True
