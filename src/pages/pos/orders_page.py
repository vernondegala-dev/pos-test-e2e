import logging

import allure

from src.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class OrdersPage(BasePage):
    SELECTORS = {
        "search_input": '.o_searchview_input',
        "order_row": '.o_data_row',
        "order_reference": '.o_field_char',
        "order_total": '.o_field_monetary',
        "order_state": '.o_field_badge',
        "order_customer": '.o_field_many2one',
        "order_date": '.o_field_date',
        "filter_button": '.o_search_options',
        "filter_draft": '.o_filter_condition:has-text("Draft")',
        "filter_done": '.o_filter_condition:has-text("Done")',
        "filter_cancel": '.o_filter_condition:has-text("Cancelled")',
        "order_detail": '.o_form_view',
        "back_button": '.o_form_button_cancel',
        "pager": '.o_pager',
        "list_view": '.o_list_view',
    }

    @allure.step("Search order: {query}")
    def search_order(self, query: str):
        self.fill(self.SELECTORS["search_input"], query)
        self.page.keyboard.press("Enter")
        self.wait_for_page_load()
        return self

    @allure.step("Open order: {order_ref}")
    def open_order(self, order_ref: str):
        self.search_order(order_ref)
        self.click(f'.o_data_row:has-text("{order_ref}")')
        self.wait_for_element(self.SELECTORS["order_detail"])
        return self

    @allure.step("Get order total")
    def get_order_total(self, order_ref: str) -> str:
        self.open_order(order_ref)
        total = self.get_text(self.SELECTORS["order_total"])
        self.click(self.SELECTORS["back_button"])
        return total

    @allure.step("Get order state: {order_ref}")
    def get_order_state(self, order_ref: str) -> str:
        self.open_order(order_ref)
        state = self.get_text(self.SELECTORS["order_state"])
        self.click(self.SELECTORS["back_button"])
        return state

    @allure.step("Get all orders")
    def get_orders(self) -> list:
        rows = self.page.locator(self.SELECTORS["order_row"]).all()
        orders = []
        for row in rows:
            orders.append({
                "reference": row.locator(self.SELECTORS["order_reference"]).inner_text(),
                "total": row.locator(self.SELECTORS["order_total"]).inner_text(),
                "state": row.locator(self.SELECTORS["order_state"]).inner_text(),
            })
        return orders

    @allure.step("Filter by state: {state}")
    def filter_by_state(self, state: str):
        self.click(self.SELECTORS["filter_button"])
        state_map = {
            "draft": self.SELECTORS["filter_draft"],
            "done": self.SELECTORS["filter_done"],
            "cancel": self.SELECTORS["filter_cancel"],
        }
        selector = state_map.get(state.lower())
        if selector:
            self.click(selector)
        self.wait_for_page_load()
        return self

    @allure.step("Count orders")
    def get_order_count(self) -> int:
        return len(self.page.locator(self.SELECTORS["order_row"]).all())

    @allure.step("Check if order exists: {order_ref}")
    def order_exists(self, order_ref: str) -> bool:
        return self.is_visible(f'.o_data_row:has-text("{order_ref}")')
