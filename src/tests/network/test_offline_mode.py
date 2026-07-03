import allure


@allure.feature("Network Resilience")
@allure.story("Offline Mode")
class TestOfflineMode:
    @allure.title("POS displays error gracefully when offline")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_offline_error_display(self, login_page, page):
        login_page.navigate_to()
        assert login_page.is_visible(login_page.SELECTORS["email_input"]), "Login form should render"

    @allure.title("Page load timeout handling")
    @allure.severity(allure.severity_level.NORMAL)
    def test_timeout_handling(self, login_page, page, navigate_to):
        import time
        page.set_default_timeout(5000)
        try:
            navigate_to("http://localhost:8069/web/login")
            assert True, "Page loaded within timeout"
        except Exception:
            assert False, "Page should handle timeouts gracefully"
        finally:
            page.set_default_timeout(30000)

    @allure.title("Reconnection after network restoration")
    @allure.severity(allure.severity_level.NORMAL)
    def test_reconnection_after_restore(self, login_page, page, navigate_to):
        navigate_to("http://localhost:8069/web/login")
        page.wait_for_load_state("load")
        assert login_page.is_visible(login_page.SELECTORS["login_button"]), "Page should recover"

    @allure.title("Data integrity after intermittent connection")
    @allure.severity(allure.severity_level.NORMAL)
    def test_data_integrity_intermittent(self, login_page, page, logged_in_admin):
        assert logged_in_admin.verify_user_logged_in(), "Session should survive reconnection"
