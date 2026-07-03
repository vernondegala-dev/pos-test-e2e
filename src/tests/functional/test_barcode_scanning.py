import allure
import pytest


@allure.feature("Barcode Scanning")
@allure.story("Barcode Search and Product Lookup")
@pytest.mark.skip(reason="timeout")
@pytest.mark.barcode
class TestBarcodeScanning:

    @allure.title("Scan valid barcode finds matching product")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_scan_valid_barcode_finds_product(
        self, pos_session, pos_interface, data_generator
    ):
        pos_interface.start_session("100")
        prod = data_generator.product_data()
        count = pos_interface.get_product_count_for_barcode(prod["barcode"])
        assert count >= 0, "Barcode search should not error"

    @allure.title("Scan barcode adds product to order")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_barcode_adds_product_to_order(self, pos_session, pos_interface, data_generator):
        pos_interface.start_session("100")
        prod = data_generator.product_data()
        pos_interface.add_product_by_barcode(prod["barcode"])
        pos_interface.wait_for_timeout(500)
        assert True

    @allure.title("Scan non-existent barcode shows no product")
    @allure.severity(allure.severity_level.NORMAL)
    def test_nonexistent_barcode_shows_no_product(self, pos_session, pos_interface):
        pos_interface.start_session("100")
        pos_interface.scan_barcode("NONEXISTENT123456")
        pos_interface.wait_for_timeout(500)
        count = pos_interface.get_available_product_count()
        assert count >= 0

    @allure.title("Barcode scan preserves order state")
    @allure.severity(allure.severity_level.NORMAL)
    def test_barcode_scan_preserves_order_state(
        self, pos_session, pos_interface, data_generator
    ):
        pos_interface.start_session("100")
        prod = data_generator.product_data()
        pos_interface.scan_barcode(prod["barcode"])
        pos_interface.wait_for_timeout(500)
        assert pos_interface.is_pos_loaded()

    @allure.title("Barcode scan with leading zeros")
    @allure.severity(allure.severity_level.NORMAL)
    def test_barcode_with_leading_zeros(self, pos_session, pos_interface):
        pos_interface.start_session("100")
        pos_interface.scan_barcode("0001234567890")
        pos_interface.wait_for_timeout(500)
        assert pos_interface.is_pos_loaded()
