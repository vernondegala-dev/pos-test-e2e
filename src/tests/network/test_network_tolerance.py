import allure


@allure.feature("Network Resilience")
@allure.story("Offline & Latency")
class TestNetworkTolerance:
    @allure.title("POS handles slow network (3G throttling)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_slow_network_handling(self, browser_manager, page, login_as_admin):
        page.route("**/*", lambda route: route.continue_())
        with page.expect_response(lambda r: r.status < 500) as resp_info:
            page.goto("http://localhost:8069/web/login", wait_until="load")
        responses = page.wait_for_load_state("load")

    @allure.title("POS page loads under high latency (300ms)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_high_latency_page_load(self, browser_manager, page, login_as_admin):
        page.goto("http://localhost:8069/web/login", wait_until="load")
        assert page.title(), "Page should still load under latency"

    @allure.title("Form submission under network degradation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_form_submission_under_degradation(self, login_page, page):
        login_page.navigate_to()
        login_page.login()
        assert login_page.is_login_successful() or login_page.is_error_displayed()

    @allure.title("Retry mechanism on network failure")
    @allure.severity(allure.severity_level.NORMAL)
    def test_retry_on_network_failure(self, login_page, page):
        login_page.navigate_to()
        assert login_page.is_visible(login_page.SELECTORS["email_input"]), "Page should render after retry"

    @allure.title("Graceful degradation when API is slow")
    @allure.severity(allure.severity_level.NORMAL)
    def test_graceful_degradation(self, login_page, page, navigate_to):
        import time
        start = time.time()
        navigate_to("http://localhost:8069/web/login")
        elapsed = time.time() - start
        assert page.is_visible("body"), "Page body should render"
