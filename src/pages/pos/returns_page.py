import allure

from src.pages.base_page import BasePage


class ReturnsPage(BasePage):
    SELECTORS = {
        "create_button": "button:has-text('Create')",
        "customer_ref_input": 'input[name="partner_id"]',
        "order_ref_input": 'input[name="order_id"]',
        "product_select": 'select[name="product_id"]',
        "return_quantity": 'input[name="product_uom_qty"]',
        "reason_select": 'select[name="reason_id"]',
        "refund_method": 'select[name="refund_method"]',
        "save_button": '.o_form_button_save',
        "validate_button": 'button:has-text("Validate")',
        "return_order_row": '.o_data_row',
        "return_state": '.o_field_badge',
        "stock_moves": '.o_group:has-text("Stock Moves")',
        "order_lines": '.o_field_one2many',
        "search_input": '.o_searchview_input',
        "credit_note_check": 'input[name="create_credit_note"]',
        "receive_products_check": 'input[name="receive_products"]',
    }

    @allure.step("Create return for order: {order_ref}")
    def create_return(self, order_ref: str, product_name: str, quantity: float = 1.0, reason: str = "Defective"):
        self.click(self.SELECTORS["create_button"])
        self.fill(self.SELECTORS["order_ref_input"], order_ref)
        self.select_option(self.SELECTORS["product_select"], product_name)
        self.fill(self.SELECTORS["return_quantity"], str(quantity))
        self.select_option(self.SELECTORS["reason_select"], reason)
        self.click(self.SELECTORS["save_button"])
        self.wait_for_page_load()
        return self

    @allure.step("Validate return order")
    def validate_return(self):
        self.click(self.SELECTORS["validate_button"])
        self.handle_dialog(accept=True)
        self.wait_for_page_load()
        return self

    @allure.step("Process refund for return")
    def process_refund(self, method: str = "direct"):
        self.select_option(self.SELECTORS["refund_method"], method)
        self.click(self.SELECTORS["save_button"])
        self.wait_for_page_load()
        return self

    @allure.step("Search return: {query}")
    def search_return(self, query: str):
        self.fill(self.SELECTORS["search_input"], query)
        self.page.keyboard.press("Enter")
        self.wait_for_page_load()
        return self

    @allure.step("Get return state")
    def get_return_state(self) -> str:
        return self.get_text(self.SELECTORS["return_state"])

    @allure.step("Create credit note for return")
    def create_credit_note(self):
        if self.is_visible(self.SELECTORS["credit_note_check"]):
            self.page.locator(self.SELECTORS["credit_note_check"]).check()
            self.click(self.SELECTORS["save_button"])
            self.wait_for_page_load()
        return self
