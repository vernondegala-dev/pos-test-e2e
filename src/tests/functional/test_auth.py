import allure
import pytest


@allure.feature("Authentication")
@allure.story("Login")
class TestAuthentication:
    @allure.title("Admin user can login successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_admin_login_success(self, auth_keywords):
        auth_keywords.login_as_admin()
        assert auth_keywords.verify_user_logged_in(), "Admin should be logged in"

    @allure.title("User can logout successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_logout(self, logged_in_admin, auth_keywords):
        auth_keywords.logout()
        assert not auth_keywords.verify_user_logged_in(), "User should be logged out"

    @allure.title("Login page displays correctly")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_page_elements(self, login_page, page):
        login_page.navigate_to()
        assert login_page.is_visible(login_page.SELECTORS["email_input"]), "Email input should be visible"
        assert login_page.is_visible(login_page.SELECTORS["password_input"]), "Password input should be visible"
        assert login_page.is_visible(login_page.SELECTORS["login_button"]), "Login button should be visible"

    @allure.title("Login with demo user credentials")
    @allure.severity(allure.severity_level.NORMAL)
    def test_demo_user_login(self, auth_keywords, login_page):
        auth_keywords.login_as_user("demo", "demo")
        assert auth_keywords.verify_user_logged_in(), "Demo user should be able to login"
        auth_keywords.logout()

    @allure.title("Database selection on multi-db setup")
    @allure.severity(allure.severity_level.NORMAL)
    def test_database_selection(self, login_page, page):
        login_page.navigate_to()
        if login_page.is_visible(login_page.SELECTORS["db_dropdown"]):
            login_page.select_database("pos_test")
            login_page.login()
            assert login_page.is_login_successful(), "Should login after database selection"
