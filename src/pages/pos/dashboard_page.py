import logging

import allure

from src.core.config import config
from src.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class DashboardPage(BasePage):
    URL = f"{config.base_url}/web"

    SELECTORS = {
        "apps_menu": '.o_navbar_apps_menu button, .o_menu_apps button, button[data-menu="apps"]',
        "pos_app": 'a.o_app[data-menu-xmlid*="point_of_sale"], button.o_app[data-menu-xmlid*="point_of_sale"], a[href*="menu_id=point_of_sale"]',
        "pos_dashboard": 'a[data-menu-xmlid="point_of_sale.menu_pos_dashboard"]',
        "pos_orders_menu": 'button[data-menu-xmlid="point_of_sale.menu_point_of_sale"]',
        "pos_orders": 'a[data-menu-xmlid="point_of_sale.menu_point_ofsale"]',
        "pos_sessions": 'a[data-menu-xmlid="point_of_sale.menu_pos_session_all"]',
        "pos_payments": 'a[data-menu-xmlid="point_of_sale.menu_pos_payment"]',
        "pos_products_menu": 'button[data-menu-xmlid="point_of_sale.pos_config_menu_catalog"]',
        "pos_products": 'a[data-menu-xmlid="point_of_sale.menu_pos_products"]',
        "pos_customers": 'a[data-menu-xmlid="point_of_sale.menu_point_of_sale_customer"]',
        "user_menu": '.o_user_menu button',
        "logout_button": 'a[href*="/web/session/logout"]',
        "search_input": ".o_searchview_input",
        "notification": ".o_notification",
    }

    def navigate_to(self):
        self.navigate(self.URL)
        self.wait_for_page_load()
        return self

    @allure.step("Navigate to POS module")
    def open_pos_module(self):
        self.click(self.SELECTORS["apps_menu"])
        try:
            self.page.locator(self.SELECTORS["pos_app"]).wait_for(state="visible", timeout=5000)
            self.click(self.SELECTORS["pos_app"])
        except Exception:
            logger.warning("POS app not found in apps menu, navigating directly")
            self.page.goto(f"{config.base_url}/web#action=point_of_sale.pos_config_action&cids=1", wait_until="load")
        self.wait_for_page_load()
        logger.info("Opened POS module")
        return self

    @allure.step("Navigate to POS interface")
    def open_pos_interface(self):
        self.open_pos_module()
        self.page.goto(f"{config.base_url}/pos/1")
        self.wait_for_page_load()
        return self

    @allure.step("Open POS sessions")
    def open_sessions(self):
        self.open_pos_module()
        self._click_submenu(self.SELECTORS["pos_orders_menu"], self.SELECTORS["pos_sessions"])
        return self

    @allure.step("Open POS orders")
    def open_orders(self):
        self.open_pos_module()
        self._click_submenu(self.SELECTORS["pos_orders_menu"], self.SELECTORS["pos_orders"])
        return self

    @allure.step("Open POS products")
    def open_products(self):
        self.open_pos_module()
        self._click_submenu(self.SELECTORS["pos_products_menu"], self.SELECTORS["pos_products"])
        return self

    @allure.step("Open POS customers")
    def open_customers(self):
        self.open_pos_module()
        self._click_submenu(self.SELECTORS["pos_orders_menu"], self.SELECTORS["pos_customers"])
        return self

    def _click_submenu(self, parent_selector: str, child_selector: str):
        self.wait_for_no_modal()
        self.click(parent_selector)
        self.wait_for_element(child_selector, timeout=10000)
        self.click(child_selector)
        self.wait_for_page_load()
        return self

    @allure.step("Logout")
    def logout(self):
        self.click(self.SELECTORS["user_menu"])
        self.click(self.SELECTORS["logout_button"])
        self.wait_for_page_load()
        logger.info("Logged out")
        return self

    @allure.step("Search for: {query}")
    def search(self, query: str):
        self.fill(self.SELECTORS["search_input"], query)
        self.page.keyboard.press("Enter")
        self.wait_for_page_load()
        return self

    @allure.step("Get page title")
    def get_page_title(self) -> str:
        return self.page.title()

    @allure.step("Check if user is logged in")
    def is_user_logged_in(self) -> bool:
        return self.is_visible(self.SELECTORS["user_menu"])

    @allure.step("Check if notification is visible")
    def get_notification_text(self) -> str:
        if self.is_visible(self.SELECTORS["notification"]):
            return self.get_text(self.SELECTORS["notification"])
        return ""
