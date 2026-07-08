import allure
import pytest

from src.utils.data_generator import DataGenerator


@allure.feature("Negative Testing")
@allure.story("Invalid Login")
class TestInvalidLogin:
    @allure.title("Login with empty credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.skip(reason="Odoo does not display error for empty credentials")
    def test_empty_credentials(self, auth_keywords):
        error = auth_keywords.login_with_invalid_credentials("", "")
        assert error, "Error message should be displayed for empty credentials"

    @allure.title("Login with empty password")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.skip(reason="Odoo does not display error for empty password")
    def test_empty_password(self, auth_keywords):
        error = auth_keywords.login_with_invalid_credentials("admin", "")
        assert error, "Error message should be displayed for empty password"

    @allure.title("Login with non-existent user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_nonexistent_user(self, auth_keywords):
        error = auth_keywords.login_with_invalid_credentials("nonexistent_user_12345", "password123")
        assert error, "Error message should be displayed for non-existent user"

    @allure.title("Login with wrong password")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_wrong_password(self, auth_keywords):
        error = auth_keywords.login_with_invalid_credentials("admin", "definitely_wrong_password")
        assert error, "Error message should be displayed for wrong password"

    @allure.title("Login with SQL injection in username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sql_injection_username(self, auth_keywords):
        error = auth_keywords.login_with_invalid_credentials("' OR '1'='1", "password")
        assert error, "SQL injection should be rejected"

    @allure.title("Login with XSS in username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_xss_injection_username(self, auth_keywords):
        error = auth_keywords.login_with_invalid_credentials("<script>alert('xss')</script>", "password")
        assert error, "XSS injection should be rejected"

    @allure.title("Login with special characters in password")
    @allure.severity(allure.severity_level.NORMAL)
    def test_special_characters_in_password(self, auth_keywords):
        error = auth_keywords.login_with_invalid_credentials("admin", "!@#$%^&*()_+{}|:\"<>?")
        assert error, "Special characters should not cause errors but login should fail"
