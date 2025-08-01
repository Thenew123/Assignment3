from Models.customer import Customer
from Models.product import Product

def test_get_existing_customer():
    customer_model = Customer()
    customer = customer_model.get_customer_by_id(2)
    assert customer is not None

def test_get_products_by_branch():
    product_model = Product()
    products = product_model.get_products_by_branch(1)
    assert isinstance(products, list)
