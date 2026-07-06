import logging
from typing import Optional

from playwright.sync_api import Page

logger = logging.getLogger(__name__)

MODAL_SELECTORS = [
    "div.modal-dialog",
    ".modal-backdrop",
    ".o_modal_overlay",
    ".popup",
    ".o_popover",
    ".modal",
]


def wait_for_no_modal(page: Page, timeout: int = 5_000):
    for selector in MODAL_SELECTORS:
        try:
            page.locator(selector).wait_for(state="hidden", timeout=timeout)
        except Exception:
            pass
