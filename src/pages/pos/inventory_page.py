import allure

from src.pages.base_page import BasePage


class InventoryPage(BasePage):
    SELECTORS = {
        "create_button": 'button:has-text("New")',
        "search_input": ".o_searchview_input",
        "product_name": 'input[name="product_id"]',
        "quantity_input": 'input[name="inventory_quantity"]',
        "location_select": 'select[name="location_id"]',
        "save_button": '.o_form_button_save',
        "inventory_row": '.o_data_row',
        "stock_count": '.o_field_float',
        "filter_button": '.o_search_options',
        "forecasted_qty": '.o_field_float[name="forecasted_qty"]',
        "reordering_rules": '.o_group:has-text("Reordering Rules")',
        "min_qty": 'input[name="minimum_quantity"]',
        "max_qty": 'input[name="maximum_quantity"]',
        "inventory_adjustment": 'button:has-text("Inventory Adjustment")',
    }

    @allure.step("Open inventory for product: {product_name}")
    def open_product_inventory(self, product_name: str):
        self.fill(self.SELECTORS["search_input"], product_name)
        self.page.keyboard.press("Enter")
        self.wait_for_page_load()
        self.click(f'.o_data_row:has-text("{product_name}")')
        self.wait_for_page_load()
        return self

    @allure.step("Update stock quantity to {qty}")
    def update_stock_quantity(self, qty: float, location: str = "Your Warehouse"):
        self.click(self.SELECTORS["create_button"])
        self.fill(self.SELECTORS["quantity_input"], str(qty))
        self.select_option(self.SELECTORS["location_select"], location)
        self.click(self.SELECTORS["save_button"])
        self.wait_for_page_load()
        return self

    @allure.step("Get current stock count")
    def get_stock_count(self) -> str:
        return self.get_text(self.SELECTORS["stock_count"])

    @allure.step("Set reordering rule: min={min_qty}, max={max_qty}")
    def set_reordering_rule(self, min_qty: float, max_qty: float):
        reordering_section = self.SELECTORS["reordering_rules"]
        if self.is_visible(reordering_section):
            self.fill(self.SELECTORS["min_qty"], str(min_qty))
            self.fill(self.SELECTORS["max_qty"], str(max_qty))
            self.click(self.SELECTORS["save_button"])
            self.wait_for_page_load()
        return self

    @allure.step("Perform inventory adjustment")
    def inventory_adjustment(self, product_name: str, actual_qty: float):
        self.click(self.SELECTORS["inventory_adjustment"])
        self.fill(self.SELECTORS["search_input"], product_name)
        self.page.keyboard.press("Enter")
        self.fill(f'.o_data_row:has-text("{product_name}") input.o_field_float', str(actual_qty))
        self.click(self.SELECTORS["save_button"])
        self.wait_for_page_load()
        return self

    @allure.step("Get forecasted quantity")
    def get_forecasted_quantity(self) -> str:
        return self.get_text(self.SELECTORS["forecasted_qty"])
