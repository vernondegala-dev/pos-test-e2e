import logging

import allure

from src.core.config import config
from src.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    URL = f"{config.base_url}/web/login"

    SELECTORS = {
        "email_input": 'input[name="login"]',
        "password_input": 'input[name="password"]',
        "login_button": 'button[type="submit"]',
        "db_dropdown": 'select[name="db"]',
        "error_message": ".alert-danger",
        "login_title": ".login-title",
        "reset_password_link": 'a[href*="/web/reset_password"]',
        "signup_link": 'a[href*="/web/signup"]',
    }

    def navigate_to(self):
        self.navigate(self.URL)
        self.wait_for_page_load()
        return self

    @allure.step("Login with credentials: {username}")
    def login(self, username: str = None, password: str = None):
        username = username or config.admin_user
        password = password or config.admin_password

        self.fill(self.SELECTORS["email_input"], username)
        self.fill(self.SELECTORS["password_input"], password)
        self.click(self.SELECTORS["login_button"])
        self.wait_for_page_load()
        logger.info(f"Login attempt with user: {username}")
        return self

    @allure.step("Check if login was successful")
    def is_login_successful(self) -> bool:
        return "web/login" not in self.current_url and "web" in self.current_url

    @allure.step("Get login error message")
    def get_error_message(self) -> str:
        return self.get_text(self.SELECTORS["error_message"])

    @allure.step("Check if error message is displayed")
    def is_error_displayed(self) -> bool:
        return self.is_visible(self.SELECTORS["error_message"])

    @allure.step("Login with invalid credentials: {username}")
    def login_expecting_failure(self, username: str, password: str):
        self.navigate_to()
        self.login(username, password)
        return self

    @allure.step("Select database: {db_name}")
    def select_database(self, db_name: str):
        if self.is_visible(self.SELECTORS["db_dropdown"]):
            self.select_option(self.SELECTORS["db_dropdown"], db_name)
        return self
