import allure

from src.pages.pos import DashboardPage
from src.pages.pos.returns_page import ReturnsPage


class ReturnsKeywords:
    def __init__(self, dashboard: DashboardPage, returns: ReturnsPage):
        self.dashboard = dashboard
        self.returns = returns

    @allure.step("Navigate to returns")
    def navigate_to_returns(self):
        self.dashboard.open_pos_module()
        return self.returns

    @allure.step("Process return for order: {order_ref}")
    def process_return(self, order_ref: str, product_name: str, quantity: float = 1.0, reason: str = "Defective"):
        self.returns.create_return(order_ref, product_name, quantity, reason)
        self.returns.validate_return()
        return self.returns

    @allure.step("Process full refund for return")
    def process_full_refund(self, method: str = "direct"):
        self.returns.process_refund(method)
        return self.returns

    @allure.step("Create credit note for returned items")
    def create_credit_note(self):
        self.returns.create_credit_note()
        return self.returns

    @allure.step("Verify return state is: {expected_state}")
    def verify_return_state(self, expected_state: str) -> bool:
        actual = self.returns.get_return_state()
        return actual.strip().lower() == expected_state.lower()

    @allure.step("Search and verify return exists")
    def verify_return_exists(self, query: str) -> bool:
        self.returns.search_return(query)
        return self.returns.is_visible(f'.o_data_row:has-text("{query}")')
