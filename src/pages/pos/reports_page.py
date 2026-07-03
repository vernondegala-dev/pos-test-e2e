import allure

from src.pages.base_page import BasePage


class ReportsPage(BasePage):
    SELECTORS = {
        "search_input": '.o_searchview_input',
        "sales_report": 'a:has-text("Sales")',
        "inventory_report": 'a:has-text("Inventory")',
        "customer_report": 'a:has-text("Customers")',
        "tax_report": 'a:has-text("Taxes")',
        "pos_report": 'a:has-text("POS Orders")',
        "date_from": 'input[name="date_from"]',
        "date_to": 'input[name="date_to"]',
        "generate_button": 'button:has-text("Generate")',
        "report_table": '.o_list_view',
        "report_chart": '.o_graph_view',
        "total_row": '.o_group_by_total',
        "export_button": 'button:has-text("Export")',
        "print_button": 'button:has-text("Print")',
        "pivot_view": '.o_pivot_view',
        "measure_select": 'select[name="measures"]',
        "group_by_select": 'select[name="group_by"]',
        "report_title": '.o_report_title',
    }

    @allure.step("Generate sales report")
    def generate_sales_report(self, date_from: str = None, date_to: str = None):
        self.click(self.SELECTORS["sales_report"])
        self.wait_for_page_load()
        if date_from:
            self.fill(self.SELECTORS["date_from"], date_from)
        if date_to:
            self.fill(self.SELECTORS["date_to"], date_to)
        self.click(self.SELECTORS["generate_button"])
        self.wait_for_page_load()
        return self

    @allure.step("Generate inventory report")
    def generate_inventory_report(self):
        self.click(self.SELECTORS["inventory_report"])
        self.wait_for_page_load()
        self.click(self.SELECTORS["generate_button"])
        self.wait_for_page_load()
        return self

    @allure.step("Generate POS report")
    def generate_pos_report(self, date_from: str = None, date_to: str = None):
        self.click(self.SELECTORS["pos_report"])
        self.wait_for_page_load()
        if date_from:
            self.fill(self.SELECTORS["date_from"], date_from)
        if date_to:
            self.fill(self.SELECTORS["date_to"], date_to)
        self.click(self.SELECTORS["generate_button"])
        self.wait_for_page_load()
        return self

    @allure.step("Get report total")
    def get_report_total(self) -> str:
        return self.get_text(self.SELECTORS["total_row"])

    @allure.step("Export report")
    def export_report(self, format: str = "xlsx"):
        self.click(self.SELECTORS["export_button"])
        self.click(f'a:has-text("{format}")')
        return self

    @allure.step("Verify report has data")
    def report_has_data(self) -> bool:
        return self.is_visible(f"{self.SELECTORS['report_table']} .o_data_row")

    @allure.step("Switch to pivot view")
    def switch_to_pivot_view(self):
        self.click(self.SELECTORS["pivot_view"])
        self.wait_for_page_load()
        return self

    @allure.step("Get report title")
    def get_report_title(self) -> str:
        return self.get_text(self.SELECTORS["report_title"])
