import allure
import pytest


@allure.feature("Negative Testing")
@allure.story("Payment Failures")
class TestPaymentFailures:
    @allure.title("Cancel payment during checkout")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cancel_payment(self, pos_session, pos_keywords):
        pos_keywords.search_and_select_product("Product A")
        pos_keywords.pos_interface.click(pos_keywords.pos_interface.SELECTORS["payment_button"])
        pos_keywords.payment_keywords.cancel_payment()
        assert pos_keywords.pos_interface.is_pos_loaded(), "POS should return to order screen after cancel"

    @allure.title("Process order with zero quantity")
    @allure.severity(allure.severity_level.NORMAL)
    def test_zero_quantity_product(self, pos_session, pos_keywords):
        pos_keywords.search_and_select_product("Product A")
        pos_keywords.pos_interface.set_quantity(0)
        assert pos_keywords.pos_interface.get_order_item_count() == 0, "Zero qty item should not appear"

    @allure.title("Attempt payment with no products in order")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_payment_with_empty_order(self, pos_session, pos_keywords):
        pos_keywords.pos_interface.click(pos_keywords.pos_interface.SELECTORS["payment_button"])
        pay_btn = pos_keywords.pos_interface.SELECTORS["validate_order_button"]
        assert not pos_keywords.pos_interface.is_enabled(pay_btn), "Validate should be disabled on empty order"

    @allure.title("Process multiple payments on single order")
    @allure.severity(allure.severity_level.NORMAL)
    def test_split_payment_invalid_amounts(self, pos_session, pos_keywords):
        pos_keywords.search_and_select_product("Product A")
        pos_keywords.payment_keywords.pay_split(cash_amount=0, bank_amount=0)
        assert pos_keywords.validate_order_total(), "Order should still be valid after invalid split"

    @allure.title("Process refund on empty order")
    @allure.severity(allure.severity_level.NORMAL)
    def test_refund_empty_order(self, pos_session, pos_keywords):
        result = pos_keywords.process_refund()
        assert result is not None, "Refund on empty order should not crash"
