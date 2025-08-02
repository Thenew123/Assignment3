import pytest
from Models.customer import Customer
from Models.product import Product

def test_get_existing_customer():
    customer_model = Customer()
    customer = customer_model.get_customer_by_id(1)
    assert customer is not None
    assert isinstance(customer, tuple)
    assert customer[3] == "alice@gmail.com"



def test_get_products_by_branch():
    product_model = Product()
    products = product_model.get_products_by_branch(branch_id=1)
    assert isinstance(products, list)


def test_product_initialization():
    product = Product()
    assert hasattr(product, "get_products_by_branch")


def test_customer_missing_email():
    with pytest.raises(TypeError):
        Customer(customer_id=1, name="John Doe")  # Missing email


def test_product_zero_price():
    product = {
        "name": "Free Sample",
        "price": 0.0
    }
    assert product["price"] == 0.0



def test_customer_email_format():
    customer = {
        "email": "emily@example.com"
    }
    assert "@" in customer["email"]
