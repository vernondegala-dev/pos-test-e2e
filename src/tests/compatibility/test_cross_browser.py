import allure
import pytest


@allure.feature("Compatibility")
@allure.story("Cross-Browser")
class TestCrossBrowser:
    @allure.title("Login page renders in Chromium")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_page_chromium(self, login_page, page):
        login_page.navigate_to()
        assert login_page.is_visible(login_page.SELECTORS["login_button"]), "Login button visible in Chromium"
        assert login_page.is_visible(login_page.SELECTORS["email_input"]), "Email input visible in Chromium"

    @allure.title("POS interface renders in Chromium")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.skip(reason="Odoo 17 POS container selector needs update")
    def test_pos_interface_chromium(self, logged_in_admin, dashboard_page, pos_keywords):
        pos = pos_keywords.open_pos()
        assert pos.is_pos_loaded(), "POS loaded in Chromium"

    @allure.title("UI renders correctly at tablet resolution (768x1024)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tablet_resolution(self, browser_manager, page, login_page):
        import time
        page.set_viewport_size({"width": 768, "height": 1024})
        time.sleep(0.5)
        login_page.navigate_to()
        assert login_page.is_visible(login_page.SELECTORS["login_button"]), "Login renders on tablet"

    @allure.title("UI renders correctly at mobile resolution (375x812)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_mobile_resolution(self, browser_manager, page, login_page):
        import time
        page.set_viewport_size({"width": 375, "height": 812})
        time.sleep(0.5)
        login_page.navigate_to()
        assert login_page.is_visible(login_page.SELECTORS["login_button"]), "Login renders on mobile"

    @allure.title("UI renders correctly at desktop HD (1920x1080)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_desktop_hd_resolution(self, browser_manager, page, login_page):
        import time
        page.set_viewport_size({"width": 1920, "height": 1080})
        time.sleep(0.5)
        login_page.navigate_to()
        assert login_page.is_visible(login_page.SELECTORS["login_button"]), "Login renders on HD desktop"
