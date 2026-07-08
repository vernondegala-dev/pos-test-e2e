import allure
import pytest


@allure.feature("Offline Resilience")
@allure.story("POS Behavior Under Network Disruption")
@pytest.mark.offline
class TestOfflineResilience:

    @allure.title("POS interface loads without errors")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_pos_loads_without_errors(self, pos_session, pos_interface):
        pos_interface.start_session("100")
        assert pos_interface.is_pos_loaded()

    @allure.title("Product list renders correctly")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.skip(reason="Navigation interrupted by reload — Odoo auto-redirect")
    def test_product_list_renders(self, pos_session, pos_interface):
        pos_interface.start_session("100")
        count = pos_interface.get_available_product_count()
        assert count > 0, "Product list should contain items"
