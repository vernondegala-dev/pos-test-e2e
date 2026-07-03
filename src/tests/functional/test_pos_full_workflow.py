import allure
import pytest


@allure.feature("POS Workflow")
@allure.story("Sales Transactions")
class TestPosFullWorkflow:
    @allure.title("POS interface loads successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_pos_interface_loads(self, logged_in_admin, pos_keywords):
        pos = pos_keywords.open_pos()
        assert pos.is_pos_loaded(), "POS interface should load"
        assert pos.get_available_product_count() > 0, "Products should be available"

    @allure.title("Complete a single product sale with cash payment")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_single_product_cash_sale(self, pos_session, pos_keywords):
        pos_keywords.quick_sale("Product A", quantity=1, payment_method="Cash")
        assert pos_keywords.validate_order_total(), "Order total should be valid"

    @allure.title("Complete a sale with multiple products")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_multi_product_sale(self, pos_session, pos_keywords):
        products = [
            {"name": "Product A", "quantity": 2},
            {"name": "Product B", "quantity": 1},
            {"name": "Product C", "quantity": 3},
        ]
        pos_keywords.create_sale_order(products, payment_method="Cash")
        assert pos_keywords.validate_order_total(), "Multi-product order total should be valid"

    @allure.title("Complete sale with bank/card payment")
    @allure.severity(allure.severity_level.NORMAL)
    def test_bank_payment_sale(self, pos_session, pos_keywords):
        pos_keywords.quick_sale("Product A", quantity=1, payment_method="Bank")
        assert pos_keywords.validate_order_total(), "Bank payment should complete successfully"

    @allure.title("Sale with customer assignment")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sale_with_customer(self, pos_session, pos_keywords):
        pos_keywords.create_sale_order(
            products=[{"name": "Product A", "quantity": 1}],
            customer="Test Customer",
            payment_method="Cash",
        )
        assert pos_keywords.validate_order_total(), "Sale with customer should complete"

    @allure.title("Apply discount to order")
    @allure.severity(allure.severity_level.NORMAL)
    def test_discount_on_order(self, pos_session, pos_keywords):
        pos_keywords.search_and_select_product("Product A")
        pos_keywords.apply_discount_to_order(10)
        assert pos_keywords.validate_order_total(), "Discounted order should have valid total"

    @allure.title("Multiple sequential orders in one session")
    @allure.severity(allure.severity_level.NORMAL)
    def test_multiple_sequential_orders(self, pos_session, pos_keywords):
        for i in range(3):
            pos_keywords.quick_sale("Product A", quantity=1, payment_method="Cash")
            assert pos_keywords.validate_order_total(), f"Order {i+1} should complete"
            pos_keywords.start_new_order()

    @allure.title("Refund processed successfully")
    @allure.severity(allure.severity_level.NORMAL)
    def test_refund_order(self, pos_session, pos_keywords):
        pos_keywords.quick_sale("Product A", quantity=1, payment_method="Cash")
        assert pos_keywords.validate_order_total(), "Original order should complete"
        pos_keywords.process_refund()
        assert pos_keywords.validate_order_total(expected_min=-9999), "Refund should process"

    @allure.title("Set quantity on order line")
    @allure.severity(allure.severity_level.NORMAL)
    def test_set_custom_quantity(self, pos_session, pos_keywords):
        pos_keywords.search_and_select_product("Product A")
        pos_keywords.pos_interface.set_quantity(5)
        assert pos_keywords.pos_interface.get_order_item_count() == 1, "One product line should exist"

    @allure.title("Search products in POS")
    @allure.severity(allure.severity_level.NORMAL)
    def test_product_search_in_pos(self, pos_session, pos_keywords):
        pos_keywords.search_and_select_product("Product A")
        assert pos_keywords.pos_interface.get_order_item_count() >= 1, "Product should be found and added"
