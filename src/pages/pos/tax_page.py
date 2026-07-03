import allure

from src.pages.base_page import BasePage


class TaxPage(BasePage):
    SELECTORS = {
        "create_button": "button:has-text('Create')",
        "tax_name": 'input[name="name"]',
        "tax_amount": 'input[name="amount"]',
        "tax_type": 'select[name="amount_type"]',
        "included_in_price": 'input[name="price_include"]',
        "affect_base": 'input[name="include_base_amount"]',
        "tax_group": 'select[name="tax_group_id"]',
        "save_button": '.o_form_button_save',
        "tax_row": '.o_data_row',
        "search_input": '.o_searchview_input',
        "edit_button": '.o_form_button_edit',
        "delete_button": '.o_form_button_delete',
        "action_dropdown": '.o_dropdown_button',
        "delete_confirm": '.modal .btn-primary',
        "tax_computation": 'select[name="tax_computation"]',
        "country_select": 'select[name="country_id"]',
    }

    @allure.step("Create a new tax: {name} = {amount}%")
    def create_tax(self, name: str, amount: float, tax_type: str = "percent", included: bool = False):
        self.click(self.SELECTORS["create_button"])
        self.fill(self.SELECTORS["tax_name"], name)
        self.fill(self.SELECTORS["tax_amount"], str(amount))
        self.select_option(self.SELECTORS["tax_type"], tax_type)
        if included:
            self.page.locator(self.SELECTORS["included_in_price"]).check()
        self.click(self.SELECTORS["save_button"])
        self.wait_for_page_load()
        return self

    @allure.step("Search tax: {query}")
    def search_tax(self, query: str):
        self.fill(self.SELECTORS["search_input"], query)
        self.page.keyboard.press("Enter")
        self.wait_for_page_load()
        return self

    @allure.step("Verify tax exists: {name}")
    def tax_exists(self, name: str) -> bool:
        return self.is_visible(f'.o_data_row:has-text("{name}")')

    @allure.step("Get tax rate")
    def get_tax_rate(self, name: str) -> str:
        self.search_tax(name)
        return self.get_text(f'.o_data_row:has-text("{name}") .o_field_float')
