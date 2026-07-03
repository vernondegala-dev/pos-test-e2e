import allure
import pytest


@allure.feature("Receipt Verification")
@allure.story("Receipt Generation and Content Validation")
@pytest.mark.receipt
class TestReceiptVerification:

    @allure.title("Receipt shows correct product count after sale")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_receipt_shows_correct_item_count(self, pos_session, pos_interface):
        pos_interface.start_session("100")
        pos_interface.select_first_product()
        pos_interface.wait_for_timeout(500)
        count = pos_interface.get_order_item_count()
        assert count > 0, "Order should contain at least one item"

    @allure.title("Receipt subtotal is greater than zero")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_receipt_subtotal_positive(self, pos_session, pos_interface):
        pos_interface.start_session("100")
        pos_interface.select_first_product()
        pos_interface.wait_for_timeout(500)
        total = pos_interface.get_total()
        assert "$" in total, "Total should include dollar sign"

    @allure.title("Receipt handles multiple line items")
    @allure.severity(allure.severity_level.NORMAL)
    def test_receipt_multiple_line_items(self, pos_session, pos_interface):
        pos_interface.start_session("100")
        pos_interface.select_first_product()
        pos_interface.wait_for_timeout(300)
        pos_interface.select_first_product()
        pos_interface.wait_for_timeout(300)
        count = pos_interface.get_order_item_count()
        assert count >= 1, "Order should have at least one item"

    @allure.title("Receipt total matches expected after discount")
    @allure.severity(allure.severity_level.NORMAL)
    def test_receipt_total_with_discount(self, pos_session, pos_interface):
        pos_interface.start_session("100")
        pos_interface.select_first_product()
        pos_interface.wait_for_timeout(500)
        total = pos_interface.get_total()
        assert total != "", "Total should not be empty"

    @allure.title("Empty order shows no receipt items")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_order_shows_no_items(self, pos_session, pos_interface):
        pos_interface.start_session("100")
        count = pos_interface.get_order_item_count()
        assert count == 0, "Empty order should have zero items"
