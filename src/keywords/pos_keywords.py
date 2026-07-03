import logging

import allure

from src.core.config import config
from src.pages.pos import PosInterfacePage, OrdersPage

logger = logging.getLogger(__name__)


class PosKeywords:
    def __init__(self, pos_interface: PosInterfacePage, orders_page: OrdersPage):
        self.pos_interface = pos_interface
        self.orders_page = orders_page

    @allure.step("Open POS interface")
    def open_pos(self, pos_id: int = 1):
        self.pos_interface.navigate_to(pos_id)
        assert self.pos_interface.is_pos_loaded(), "POS interface did not load"
        logger.info(f"POS interface opened (config_id: {pos_id})")
        return self.pos_interface

    @allure.step("Create a sale order with multiple products")
    def create_sale_order(self, products: list, customer: str = None, payment_method: str = "Cash"):
        result = self.pos_interface.complete_sale(products, payment_method, customer)
        logger.info(f"Sale order created with {len(products)} product(s) via {payment_method}")
        return result

    @allure.step("Create a quick sale with single product")
    def quick_sale(self, product_name: str, quantity: int = 1, payment_method: str = "Cash"):
        products = [{"name": product_name, "quantity": quantity}]
        return self.create_sale_order(products, payment_method=payment_method)

    @allure.step("Verify order exists in backend")
    def verify_order_in_backend(self, order_reference: str) -> bool:
        return self.orders_page.order_exists(order_reference)

    @allure.step("Get order total")
    def get_order_total(self, order_reference: str) -> str:
        return self.orders_page.get_order_total(order_reference)

    @allure.step("Get order count")
    def get_order_count(self) -> int:
        return self.orders_page.get_order_count()

    @allure.step("Process refund for last order")
    def process_refund(self):
        self.pos_interface.process_refund()
        logger.info("Refund processed")
        return self.pos_interface

    @allure.step("Set customer on order")
    def set_customer_on_order(self, customer_name: str):
        self.pos_interface.set_customer(customer_name)
        return self.pos_interface

    @allure.step("Apply discount to order")
    def apply_discount_to_order(self, percentage: float):
        self.pos_interface.apply_discount(percentage)
        return self.pos_interface

    @allure.step("Send receipt by email")
    def send_receipt_email(self, email: str):
        self.pos_interface.email_receipt(email)
        return self.pos_interface

    @allure.step("Start a new order")
    def start_new_order(self):
        self.pos_interface.new_order()
        return self.pos_interface

    @allure.step("Get POS product count")
    def get_available_products_count(self) -> int:
        return self.pos_interface.get_available_product_count()

    @allure.step("Close POS session")
    def close_pos_session(self):
        self.pos_interface.close_session()
        return self.pos_interface

    @allure.step("Validate order total display")
    def validate_order_total(self, expected_min: float = 0) -> bool:
        total_text = self.pos_interface.get_total()
        try:
            total = float(total_text.replace("$", "").replace(",", "").strip())
            return total > expected_min
        except (ValueError, AttributeError):
            logger.warning(f"Could not parse total: {total_text}")
            return False

    @allure.step("Search and select product in POS")
    def search_and_select_product(self, product_name: str):
        self.pos_interface.search_product(product_name)
        self.pos_interface.select_product(product_name)
        return self.pos_interface
