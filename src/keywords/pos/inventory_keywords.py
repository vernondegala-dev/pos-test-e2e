import allure

from src.pages.pos import DashboardPage
from src.pages.pos.inventory_page import InventoryPage


class InventoryKeywords:
    def __init__(self, dashboard: DashboardPage, inventory: InventoryPage):
        self.dashboard = dashboard
        self.inventory = inventory

    @allure.step("Navigate to inventory")
    def navigate_to_inventory(self):
        self.dashboard.open_pos_module()
        return self.inventory

    @allure.step("Update product stock: {product_name} -> {qty}")
    def update_product_stock(self, product_name: str, qty: float):
        self.inventory.open_product_inventory(product_name)
        self.inventory.update_stock_quantity(qty)
        return self.inventory

    @allure.step("Verify stock level: {product_name}")
    def verify_stock_level(self, product_name: str) -> str:
        self.inventory.open_product_inventory(product_name)
        return self.inventory.get_stock_count()

    @allure.step("Configure reordering rule for {product_name}")
    def configure_reordering_rule(self, product_name: str, min_qty: float, max_qty: float):
        self.inventory.open_product_inventory(product_name)
        self.inventory.set_reordering_rule(min_qty, max_qty)
        return self.inventory

    @allure.step("Perform inventory adjustment count")
    def perform_inventory_count(self, product_name: str, actual_qty: float):
        self.inventory.inventory_adjustment(product_name, actual_qty)
        return self.inventory

    @allure.step("Get forecasted quantity for {product_name}")
    def get_forecasted_quantity(self, product_name: str) -> str:
        self.inventory.open_product_inventory(product_name)
        return self.inventory.get_forecasted_quantity()
