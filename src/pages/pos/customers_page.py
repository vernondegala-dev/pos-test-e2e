import logging

import allure

from src.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CustomersPage(BasePage):
    SELECTORS = {
        "create_button": "button:has-text('Create')",
        "import_button": '.o_button_import',
        "search_input": '.o_searchview_input',
        "form_view": '.o_form_view',
        "list_view": '.o_list_view',
        "name_input": 'input[name="name"]',
        "email_input": 'input[name="email"]',
        "phone_input": 'input[name="phone"]',
        "mobile_input": 'input[name="mobile"]',
        "street_input": 'input[name="street"]',
        "city_input": 'input[name="city"]',
        "zip_input": 'input[name="zip"]',
        "country_select": 'select[name="country_id"]',
        "vat_input": 'input[name="vat"]',
        "company_input": 'input[name="company_name"]',
        "save_button": '.o_form_button_save',
        "discard_button": '.o_form_button_discard',
        "edit_button": '.o_form_button_edit',
        "delete_button": '.o_form_button_delete',
        "action_dropdown": '.o_dropdown_button',
        "delete_confirm": '.modal .btn-primary',
        "customer_row": '.o_data_row',
        "customer_name_cell": '.o_field_char',
    }

    @allure.step("Click Create Customer")
    def click_create(self):
        self.click(self.SELECTORS["create_button"])
        self.wait_for_element(self.SELECTORS["form_view"])
        return self

    @allure.step("Fill customer form with data")
    def fill_customer_form(self, customer_data: dict):
        if "name" in customer_data:
            self.fill(self.SELECTORS["name_input"], customer_data["name"])
        if "email" in customer_data:
            self.fill(self.SELECTORS["email_input"], customer_data["email"])
        if "phone" in customer_data:
            self.fill(self.SELECTORS["phone_input"], customer_data["phone"])
        if "mobile" in customer_data:
            self.fill(self.SELECTORS["mobile_input"], customer_data["mobile"])
        if "street" in customer_data:
            self.fill(self.SELECTORS["street_input"], customer_data["street"])
        if "city" in customer_data:
            self.fill(self.SELECTORS["city_input"], customer_data["city"])
        if "zip" in customer_data:
            self.fill(self.SELECTORS["zip_input"], customer_data["zip"])
        if "country" in customer_data:
            self.select_option(self.SELECTORS["country_select"], customer_data["country"])
        if "vat" in customer_data:
            self.fill(self.SELECTORS["vat_input"], customer_data["vat"])
        if "company" in customer_data:
            self.fill(self.SELECTORS["company_input"], customer_data["company"])
        return self

    @allure.step("Save customer form")
    def save(self):
        self.click(self.SELECTORS["save_button"])
        self.wait_for_page_load()
        return self

    @allure.step("Create a new customer")
    def create_customer(self, customer_data: dict):
        self.click_create()
        self.fill_customer_form(customer_data)
        self.save()
        return self

    @allure.step("Search customer: {query}")
    def search_customer(self, query: str):
        self.fill(self.SELECTORS["search_input"], query)
        self.page.keyboard.press("Enter")
        self.wait_for_page_load()
        return self

    @allure.step("Check if customer exists: {customer_name}")
    def customer_exists(self, customer_name: str) -> bool:
        return self.is_visible(f'.o_data_row:has-text("{customer_name}")')

    @allure.step("Delete customer: {customer_name}")
    def delete_customer(self, customer_name: str):
        self.search_customer(customer_name)
        self.click(f'.o_data_row:has-text("{customer_name}")')
        self.wait_for_element(self.SELECTORS["form_view"])
        self.click(self.SELECTORS["action_dropdown"])
        self.click(self.SELECTORS["delete_button"])
        self.click(self.SELECTORS["delete_confirm"])
        self.wait_for_page_load()
        return self

    @allure.step("Edit customer: {customer_name}")
    def edit_customer(self, customer_name: str, updates: dict):
        self.search_customer(customer_name)
        self.click(f'.o_data_row:has-text("{customer_name}")')
        self.wait_for_element(self.SELECTORS["form_view"])
        self.click(self.SELECTORS["edit_button"])
        self.fill_customer_form(updates)
        self.save()
        return self

    @allure.step("Get customer count")
    def get_customer_count(self) -> int:
        return len(self.page.locator(self.SELECTORS["customer_row"]).all())
