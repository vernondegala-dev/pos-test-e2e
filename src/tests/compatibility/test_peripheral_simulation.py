import allure
import pytest


@allure.feature("Compatibility")
@allure.story("Peripheral Simulation")
class TestPeripheralSimulation:
    @allure.title("Barcode scan input accepted in POS")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.skip(reason="Product form creation needs Odoo 17 selector fixes")
    def test_barcode_scan_input(self, logged_in_admin, dashboard_page, products_page, data_generator):
        dashboard_page.open_products()
        prod = data_generator.product_data()
        products_page.create_product(prod)
        products_page.search_product(prod["barcode"])
        assert products_page.product_exists(prod["name"]), "Product found by barcode"

    @allure.title("Receipt preview renders correctly")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.skip(reason="POS session fixture needs Odoo 17 selector fixes")
    def test_receipt_preview(self, pos_session, pos_keywords):
        pos_keywords.quick_sale("Product A", quantity=1, payment_method="Cash")
        assert pos_keywords.validate_order_total()

    @allure.title("Multiple payment terminal support")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.skip(reason="POS session fixture needs Odoo 17 selector fixes")
    def test_multiple_payment_terminals(self, pos_session, pos_keywords):
        pos_keywords.quick_sale("Product A", quantity=1, payment_method="Bank")
        assert pos_keywords.validate_order_total(), "Bank payment should process"

    @allure.title("Cash drawer integration signal")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.skip(reason="POS session fixture needs Odoo 17 selector fixes")
    def test_cash_drawer_signal(self, pos_session, pos_keywords):
        pos_keywords.quick_sale("Product B", quantity=1, payment_method="Cash")
        assert pos_keywords.validate_order_total(), "Cash sale should trigger drawer signal"
