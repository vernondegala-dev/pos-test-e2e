import logging
import os
from pathlib import Path
from typing import Optional

from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from src.core.config import config
from src.core.self_healing.locator_manager import LocatorManager

logger = logging.getLogger(__name__)


class BrowserManager:
    def __init__(self):
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

    def start(self) -> Page:
        self._playwright = sync_playwright().start()
        browser_type = getattr(self._playwright, config.browser, None)
        if not browser_type:
            available = ["chromium", "firefox", "webkit"]
            fallback = "chromium"
            logger.warning(f"Browser '{config.browser}' not found. Using {fallback}. Available: {available}")
            browser_type = getattr(self._playwright, fallback)

        self._browser = browser_type.launch(**config.as_playwright_launch_options())
        self._context = self._browser.new_context(
            viewport={"width": config.viewport_width, "height": config.viewport_height},
            locale="en-US",
            timezone_id="America/New_York",
            permissions=["clipboard-read", "clipboard-write"],
            ignore_https_errors=True,
        )
        self._context.set_default_timeout(config.timeout)
        self._page = self._context.new_page()
        self._page.set_default_timeout(config.timeout)
        logger.info(f"Browser started: {config.browser} (headless={config.headless})")
        return self._page

    @property
    def page(self) -> Page:
        if self._page is None:
            raise RuntimeError("Browser not started. Call start() first.")
        return self._page

    @property
    def locator_manager(self) -> LocatorManager:
        return LocatorManager(self.page)

    def take_screenshot(self, name: str) -> str:
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(exist_ok=True)
        path = str(screenshot_dir / f"{name}.png")
        self.page.screenshot(path=path, full_page=True)
        logger.info(f"Screenshot saved: {path}")
        return path

    def start_tracing(self):
        if not self._context:
            logger.warning("Cannot start tracing: no context")
            return
        trace_dir = Path("reports/traces")
        trace_dir.mkdir(parents=True, exist_ok=True)
        self._context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True,
        )

    def stop_tracing(self, name: str = "trace"):
        if not self._context:
            logger.warning("Cannot stop tracing: no context")
            return ""
        trace_dir = Path("reports/traces")
        trace_dir.mkdir(parents=True, exist_ok=True)
        path = str(trace_dir / f"{name}.zip")
        try:
            self._context.tracing.stop(path=path)
        except Exception as e:
            logger.warning(f"Failed to stop tracing: {e}")
            return ""
        return path

    def close(self):
        try:
            if self._context:
                self._context.close()
            if self._browser:
                self._browser.close()
            if self._playwright:
                self._playwright.stop()
        except Exception as e:
            logger.warning(f"Error closing browser: {e}")
        finally:
            self._playwright = None
            self._browser = None
            self._context = None
            self._page = None
        logger.info("Browser closed.")
