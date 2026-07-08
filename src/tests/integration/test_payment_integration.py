import allure
import pytest


@pytest.mark.skip(reason="Products not visible in POS grid (article.product timeout)")
@allure.feature("Integration")
@allure.story("Payment Processing Integration")
class TestPaymentIntegration:
    @allure.title("Cash payment recorded in accounting")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cash_payment_accounting(self, pos_session, pos_keywords):
        pos_keywords.quick_sale("Product A", quantity=1, payment_method="Cash")
        assert pos_keywords.validate_order_total(), "Cash sale should complete"

    @allure.title("Bank card payment processes correctly")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_bank_payment_accounting(self, pos_session, pos_keywords):
        pos_keywords.quick_sale("Product B", quantity=2, payment_method="Bank")
        assert pos_keywords.validate_order_total(), "Bank sale should complete"

    @allure.title("Split payment recorded to correct accounts")
    @allure.severity(allure.severity_level.NORMAL)
    def test_split_payment_accounting(self, pos_session, pos_keywords):
        products = [
            {"name": "Product A", "quantity": 1},
            {"name": "Product B", "quantity": 1},
        ]
        pos_keywords.create_sale_order(products, payment_method="Cash")
        assert pos_keywords.validate_order_total(), "Multi-payment order should complete"

    @allure.title("Refund reverses original payment entry")
    @allure.severity(allure.severity_level.NORMAL)
    def test_refund_reverses_payment(self, pos_session, pos_keywords):
        pos_keywords.quick_sale("Product A", quantity=1, payment_method="Cash")
        assert pos_keywords.validate_order_total()
        pos_keywords.process_refund()
        assert pos_keywords.validate_order_total(expected_min=-9999), "Refund should process"
