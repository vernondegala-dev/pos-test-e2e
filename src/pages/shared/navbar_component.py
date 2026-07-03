import logging

import allure

from src.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class NavbarComponent(BasePage):
    SELECTORS = {
        "apps_menu": '.o_menu_sections a[data-menu-xmlid="base.menu_apps"]',
        "user_menu": ".o_user_menu",
        "user_avatar": ".o_user_avatar",
        "user_name": ".o_user_name",
        "logout_button": 'a[data-menu="logout"]',
        "settings_link": 'a[data-menu-xmlid="base.menu_administration"]',
        "search_input": ".o_searchview_input",
        "notification_icon": ".o_notification_icon",
        "notification_popover": ".o_notification_popover",
        "breadcrumb": ".o_breadcrumb",
        "home_link": ".o_home_menu",
        "menu_section": ".o_menu_sections",
    }

    @allure.step("Open apps menu")
    def open_apps_menu(self):
        self.click(self.SELECTORS["apps_menu"])
        return self

    @allure.step("Open user menu")
    def open_user_menu(self):
        self.click(self.SELECTORS["user_menu"])
        return self

    @allure.step("Logout")
    def logout(self):
        self.open_user_menu()
        self.click(self.SELECTORS["logout_button"])
        self.wait_for_page_load()
        logger.info("Logged out via navbar")
        return self

    @allure.step("Get logged-in user name")
    def get_user_name(self) -> str:
        self.open_user_menu()
        name = self.get_text(self.SELECTORS["user_name"])
        self.click(self.SELECTORS["user_menu"])
        return name

    @allure.step("Navigate to app by menu xmlid: {menu_xmlid}")
    def navigate_to_app(self, menu_xmlid: str):
        self.open_apps_menu()
        self.click(f'a[data-menu-xmlid="{menu_xmlid}"]')
        self.wait_for_page_load()
        return self

    @allure.step("Search: {query}")
    def search(self, query: str):
        self.fill(self.SELECTORS["search_input"], query)
        self.page.keyboard.press("Enter")
        self.wait_for_page_load()
        return self

    @allure.step("Go Home")
    def go_home(self):
        self.click(self.SELECTORS["home_link"])
        self.wait_for_page_load()
        return self

    @allure.step("Get current breadcrumb text")
    def get_breadcrumb_text(self) -> str:
        return self.get_text(self.SELECTORS["breadcrumb"])
