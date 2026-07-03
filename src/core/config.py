import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Config:
    base_url: str = field(default_factory=lambda: os.getenv("BASE_URL", "http://localhost:8069"))
    admin_user: str = field(default_factory=lambda: os.getenv("ADMIN_USER", "admin"))
    admin_password: str = field(default_factory=lambda: os.getenv("ADMIN_PASSWORD", "admin"))
    db_name: str = field(default_factory=lambda: os.getenv("DB_NAME", "pos_test"))

    browser: str = field(default_factory=lambda: os.getenv("BROWSER", "chromium"))
    headless: bool = field(default_factory=lambda: os.getenv("HEADLESS", "true").lower() == "true")
    viewport_width: int = int(os.getenv("VIEWPORT_WIDTH", "1920"))
    viewport_height: int = int(os.getenv("VIEWPORT_HEIGHT", "1080"))
    slow_mo: int = int(os.getenv("SLOW_MO", "0"))
    timeout: int = int(os.getenv("TIMEOUT", "30000"))

    retry_max_attempts: int = int(os.getenv("RETRY_MAX_ATTEMPTS", "3"))
    retry_base_delay: float = float(os.getenv("RETRY_BASE_DELAY", "1.0"))
    retry_max_delay: float = float(os.getenv("RETRY_MAX_DELAY", "10.0"))

    screenshot_on_failure: bool = field(default_factory=lambda: os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true")
    video_on_failure: bool = field(default_factory=lambda: os.getenv("VIDEO_ON_FAILURE", "true").lower() == "true")
    trace_on_failure: bool = field(default_factory=lambda: os.getenv("TRACE_ON_FAILURE", "true").lower() == "true")

    allure_report_dir: str = field(default_factory=lambda: os.getenv("ALLURE_REPORT_DIR", "reports/allure-results"))
    junit_report_dir: str = field(default_factory=lambda: os.getenv("JUNIT_REPORT_DIR", "reports/junit"))

    perf_threshold_lcp: int = int(os.getenv("PERF_THRESHOLD_LCP", "2500"))
    perf_threshold_fid: int = int(os.getenv("PERF_THRESHOLD_FID", "100"))
    perf_threshold_cls: float = float(os.getenv("PERF_THRESHOLD_CLS", "0.1"))
    perf_threshold_page_load: int = int(os.getenv("PERF_THRESHOLD_PAGE_LOAD", "3000"))

    k6_base_url: str = field(default_factory=lambda: os.getenv("K6_BASE_URL", "http://localhost:8069"))
    k6_vus: int = int(os.getenv("K6_VUS", "10"))
    k6_duration: str = field(default_factory=lambda: os.getenv("K6_DURATION", "30s"))

    @property
    def odoo_pos_url(self) -> str:
        return f"{self.base_url}/pos"

    @property
    def odoo_web_url(self) -> str:
        return f"{self.base_url}/web"

    def as_playwright_launch_options(self) -> dict:
        return {
            "headless": self.headless,
            "slow_mo": self.slow_mo,
            "timeout": self.timeout,
            "args": ["--disable-dev-shm-usage", "--no-sandbox", "--disable-setuid-sandbox"],
        }


config = Config()
