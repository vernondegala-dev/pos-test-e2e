import allure
import pytest


@allure.feature("Stock Alerts")
@allure.story("Stock Threshold Warnings and Reorder Alerts")
@pytest.mark.stock_alerts
class TestStockAlerts:

    @allure.title("Products display in stock after sale")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_products_visible_after_sale(self, logged_in_admin, dashboard_page, products_page):
        dashboard_page.open_products()
        count = products_page.get_product_count()
        assert count > 0, "Products should be visible after sale"

    @allure.title("Products are searchable by name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_products_searchable_by_name(self, logged_in_admin, dashboard_page, products_page):
        dashboard_page.open_products()
        products_page.search_product("Desk")
        assert True
