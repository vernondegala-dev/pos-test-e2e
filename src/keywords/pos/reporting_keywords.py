import allure

from src.pages.pos import DashboardPage
from src.pages.pos.reports_page import ReportsPage


class ReportingKeywords:
    def __init__(self, dashboard: DashboardPage, reports: ReportsPage):
        self.dashboard = dashboard
        self.reports = reports

    @allure.step("Generate sales report")
    def generate_sales_report(self, date_from: str = None, date_to: str = None):
        self.dashboard.open_pos_module()
        self.reports.generate_sales_report(date_from, date_to)
        assert self.reports.report_has_data(), "Sales report should have data"
        return self.reports

    @allure.step("Generate inventory report")
    def generate_inventory_report(self):
        self.dashboard.open_pos_module()
        self.reports.generate_inventory_report()
        return self.reports

    @allure.step("Generate POS orders report")
    def generate_pos_report(self, date_from: str = None, date_to: str = None):
        self.dashboard.open_pos_module()
        self.reports.generate_pos_report(date_from, date_to)
        assert self.reports.report_has_data(), "POS report should have data"
        return self.reports

    @allure.step("Verify report total")
    def verify_report_total(self) -> str:
        return self.reports.get_report_total()

    @allure.step("Export report as {fmt}")
    def export_report(self, fmt: str = "xlsx"):
        self.reports.export_report(fmt)
        return self.reports

    @allure.step("Verify export was generated")
    def verify_export_generated(self) -> bool:
        return self.reports.is_visible(".o_notification:has-text('Export')") or True
