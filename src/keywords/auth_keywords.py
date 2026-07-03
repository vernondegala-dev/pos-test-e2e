import logging

import allure

from src.core.config import config
from src.pages.pos import LoginPage, DashboardPage

logger = logging.getLogger(__name__)


class AuthKeywords:
    def __init__(self, login_page: LoginPage, dashboard_page: DashboardPage):
        self.login_page = login_page
        self.dashboard_page = dashboard_page

    @allure.step("Login as admin")
    def login_as_admin(self) -> DashboardPage:
        self.login_page.navigate_to()
        self.login_page.login(config.admin_user, config.admin_password)
        assert self.login_page.is_login_successful(), "Admin login failed"
        logger.info("Admin login successful")
        return self.dashboard_page

    @allure.step("Login as user: {username}")
    def login_as_user(self, username: str, password: str) -> DashboardPage:
        self.login_page.navigate_to()
        self.login_page.login(username, password)
        assert self.login_page.is_login_successful(), f"Login failed for user: {username}"
        logger.info(f"Login successful for user: {username}")
        return self.dashboard_page

    @allure.step("Login with invalid credentials expecting failure")
    def login_with_invalid_credentials(self, username: str, password: str):
        self.login_page.navigate_to()
        self.login_page.login(username, password)
        assert self.login_page.is_error_displayed(), "Expected error message but none displayed"
        error_text = self.login_page.get_error_message()
        logger.info(f"Login failed as expected. Error: {error_text}")
        return error_text

    @allure.step("Logout")
    def logout(self):
        self.dashboard_page.logout()
        assert "web/login" in self.dashboard_page.current_url, "Logout failed"
        logger.info("Logout successful")

    @allure.step("Verify user is logged in")
    def verify_user_logged_in(self) -> bool:
        return self.dashboard_page.is_user_logged_in()

    @allure.step("Get current username from UI")
    def get_current_username(self) -> str:
        return self.dashboard_page.get_page_title()
