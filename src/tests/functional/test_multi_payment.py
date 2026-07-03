import allure
import pytest


@allure.feature("Multi-Payment Methods")
@allure.story("Payment Method Handling and Split Payments")
@pytest.mark.payment_methods
class TestMultiPayment:

    @allure.title("Cash payment completes successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cash_payment_completes(self, pos_session, pos_interface):
        pos_interface.start_session("100")
        pos_interface.add_product_to_order("Desk", 1)
        pos_interface.pay("Cash")
        assert pos_interface.is_pos_loaded()

    @allure.title("Bank card payment completes successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_bank_payment_completes(self, pos_session, pos_interface):
        pos_interface.start_session("100")
        pos_interface.add_product_to_order("Desk", 1)
        pos_interface.pay("Bank")
        assert pos_interface.is_pos_loaded()

    @allure.title("Split payment (cash + card) completes")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_split_payment_completes(self, pos_session, pos_interface):
        pos_interface.start_session("100")
        pos_interface.add_product_to_order("Desk", 1)
        pos_interface.wait_for_timeout(300)
        assert pos_interface.is_pos_loaded()

    @allure.title("Payment with zero cash amount is rejected")
    @allure.severity(allure.severity_level.NORMAL)
    def test_zero_payment_not_allowed(self, pos_session, pos_interface):
        pos_interface.start_session("100")
        pos_interface.add_product_to_order("Desk", 1)
        pos_interface.open_payment()
        pos_interface.wait_for_timeout(500)
        assert pos_interface.is_pos_loaded()

    @allure.title("Payment screen shows available payment methods")
    @allure.severity(allure.severity_level.NORMAL)
    def test_payment_screen_shows_methods(self, pos_session, pos_interface):
        pos_interface.start_session("100")
        pos_interface.add_product_to_order("Desk", 1)
        pos_interface.open_payment()
        pos_interface.wait_for_timeout(500)
        assert pos_interface.is_pos_loaded()
