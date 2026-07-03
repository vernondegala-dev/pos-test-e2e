import logging

import allure

from src.pages.pos import PosInterfacePage

logger = logging.getLogger(__name__)


class PaymentKeywords:
    def __init__(self, pos_interface: PosInterfacePage):
        self.pos_interface = pos_interface

    @allure.step("Pay order with Cash")
    def pay_with_cash(self):
        self.pos_interface.pay("Cash")
        logger.info("Paid with Cash")
        return self.pos_interface

    @allure.step("Pay order with Bank/Card")
    def pay_with_bank(self):
        self.pos_interface.pay("Bank")
        logger.info("Paid with Bank")
        return self.pos_interface

    @allure.step("Pay with split payment (cash + bank)")
    def pay_split(self, cash_amount: float, bank_amount: float):
        self.pos_interface.pay_split(cash_amount, bank_amount)
        logger.info(f"Split payment: Cash=${cash_amount}, Bank=${bank_amount}")
        return self.pos_interface

    @allure.step("Validate payment was successful")
    def validate_payment_success(self) -> bool:
        try:
            self.pos_interface.wait_for_text("Order", timeout=5000)
            return True
        except Exception:
            return False

    @allure.step("Get total amount due")
    def get_amount_due(self) -> float:
        text = self.pos_interface.get_total()
        if text:
            try:
                return float(text.replace("$", "").replace(",", "").strip())
            except (ValueError, AttributeError):
                pass
        return 0.0

    @allure.step("Cancel payment")
    def cancel_payment(self):
        self.pos_interface.click(".cancel-payment")
        return self.pos_interface
