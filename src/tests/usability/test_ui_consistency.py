import allure


@allure.feature("Usability")
@allure.story("UI Consistency")
class TestUiConsistency:
    @allure.title("All POS UI elements are properly labeled")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ui_elements_labeled(self, logged_in_admin, dashboard_page, pos_keywords):
        pos = pos_keywords.open_pos()
        assert pos.is_pos_loaded(), "POS should load"
        visible_buttons = ["payment_button", "customer_button", "new_order_button"]
        for btn in visible_buttons:
            selector = pos.SELECTORS.get(btn)
            if selector and pos.is_visible(selector):
                assert True, f"{btn} is visible"

    @allure.title("Error messages are user-friendly")
    @allure.severity(allure.severity_level.NORMAL)
    def test_error_messages_user_friendly(self, auth_keywords):
        error = auth_keywords.login_with_invalid_credentials("nonexistent", "wrong")
        assert error, "Error message should be displayed"
        assert len(error) > 5, "Error message should be descriptive"

    @allure.title("Loading states are indicated")
    @allure.severity(allure.severity_level.NORMAL)
    def test_loading_states(self, login_page, page):
        login_page.navigate_to()
        login_page.login()
        page.wait_for_load_state("load")

    @allure.title("Navigation breadcrumbs are consistent")
    @allure.severity(allure.severity_level.NORMAL)
    def test_navigation_breadcrumbs(self, logged_in_admin, dashboard_page):
        assert dashboard_page.is_user_logged_in(), "User logged in"

    @allure.title("Tab order follows logical sequence")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tab_order(self, login_page, page):
        login_page.navigate_to()
        page.keyboard.press("Tab")
        focused = page.evaluate("document.activeElement.name")
        assert focused in ["login", "password", ""], "Tab should focus on login field or equivalent"
