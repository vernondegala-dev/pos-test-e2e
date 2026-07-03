import allure
import pytest


@allure.feature("Negative Testing")
@allure.story("Data Validation")
class TestDataValidation:
    @allure.title("Create product with empty name")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_product_empty_name(self, logged_in_admin, dashboard_page, product_keywords, data_generator):
        dashboard_page.open_products()
        invalid_data = data_generator.invalid_product_data(name="", price=10)
        product_keywords.create_product_expecting_failure(invalid_data)

    @allure.title("Create product with negative price")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_product_negative_price(self, logged_in_admin, dashboard_page, product_keywords, data_generator):
        dashboard_page.open_products()
        invalid_data = data_generator.invalid_product_data(name="Test Product Neg", price=-50)
        product_keywords.create_product_expecting_failure(invalid_data)

    @allure.title("Create product with extremely long name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_product_very_long_name(self, logged_in_admin, dashboard_page, product_keywords, data_generator):
        dashboard_page.open_products()
        long_name = "A" * 1000
        invalid_data = data_generator.invalid_product_data(name=long_name, price=10)
        product_keywords.create_product_expecting_failure(invalid_data)

    @allure.title("Create product with zero price")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_product_zero_price(self, logged_in_admin, dashboard_page, product_keywords, data_generator):
        dashboard_page.open_products()
        prod = data_generator.product_data(price=0)
        product_keywords.create_product(**prod)
        assert product_keywords.verify_product_exists(prod["name"]), "Product with zero price may be valid"
        product_keywords.delete_product(prod["name"])

    @allure.title("Create customer with invalid email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_customer_invalid_email(self, logged_in_admin, dashboard_page, customer_keywords, data_generator):
        dashboard_page.open_customers()
        customer_data = data_generator.customer_data(email="not-an-email")
        customer_keywords.create_customer(**customer_data)
        assert customer_keywords.verify_customer_exists(customer_data["name"])

    @allure.title("Create customer with empty name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_customer_empty_name(self, logged_in_admin, dashboard_page, customer_keywords):
        dashboard_page.open_customers()
        try:
            customer_keywords.create_customer(name="", email="test@example.com")
            pytest.fail("Creating customer with empty name should fail")
        except (AssertionError, Exception):
            pass

    @allure.title("Delete non-existent product")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_nonexistent_product(self, logged_in_admin, dashboard_page, product_keywords):
        dashboard_page.open_products()
        try:
            product_keywords.delete_product("__nonexistent_product_12345__")
            pytest.fail("Deleting non-existent product should raise error")
        except (AssertionError, Exception):
            pass
