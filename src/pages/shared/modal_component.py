import logging

import allure

from src.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class ModalComponent(BasePage):
    SELECTORS = {
        "modal": ".modal",
        "modal_dialog": ".modal-dialog",
        "modal_content": ".modal-content",
        "modal_header": ".modal-header",
        "modal_body": ".modal-body",
        "modal_footer": ".modal-footer",
        "modal_title": ".modal-title",
        "close_button": ".modal .close",
        "confirm_button": ".modal .btn-primary",
        "cancel_button": ".modal .btn-secondary",
        "dismiss_button": ".modal .btn-close",
    }

    @allure.step("Wait for modal to appear")
    def wait_for_modal(self, timeout: int = None):
        self.wait_for_element(self.SELECTORS["modal"], timeout=timeout)
        return self

    @allure.step("Get modal title")
    def get_title(self) -> str:
        return self.get_text(self.SELECTORS["modal_title"])

    @allure.step("Get modal body text")
    def get_body_text(self) -> str:
        return self.get_text(self.SELECTORS["modal_body"])

    @allure.step("Confirm modal action")
    def confirm(self):
        self.click(self.SELECTORS["confirm_button"])
        self.wait_for_page_load()
        return self

    @allure.step("Cancel modal")
    def cancel(self):
        self.click(self.SELECTORS["cancel_button"])
        return self

    @allure.step("Dismiss modal")
    def dismiss(self):
        self.click(self.SELECTORS["dismiss_button"])
        return self

    @allure.step("Close modal via X button")
    def close(self):
        self.click(self.SELECTORS["close_button"])
        return self

    @allure.step("Check if modal is displayed")
    def is_displayed(self) -> bool:
        return self.is_visible(self.SELECTORS["modal"])

    @allure.step("Fill input in modal: {locator} = {value}")
    def fill_input(self, locator: str, value: str):
        modal_locator = f"{self.SELECTORS['modal_body']} {locator}"
        self.fill(modal_locator, value)
        return self

    @allure.step("Click element inside modal: {locator}")
    def click_inside(self, locator: str):
        modal_locator = f"{self.SELECTORS['modal']} {locator}"
        self.click(modal_locator)
        return self
