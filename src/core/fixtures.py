import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Callable

import allure
import pytest

from src.core.browser_manager import BrowserManager
from src.core.config import config

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def browser_manager() -> BrowserManager:
    bm = BrowserManager()
    yield bm
    bm.close()


@pytest.fixture(autouse=True)
def setup_teardown(request, browser_manager: BrowserManager):
    page = browser_manager.start()

    if hasattr(request, "node_id"):
        test_name = request.node_id.replace("::", "_").replace("/", "_").replace("[", "_").replace("]", "_")
    else:
        test_name = f"test_{int(time.time())}"

    yield page

    try:
        if request.node.rep_call.failed:
            if config.screenshot_on_failure:
                path = browser_manager.take_screenshot(f"FAILED_{test_name}")
                allure.attach.file(path, name="failure_screenshot", attachment_type=allure.attachment_type.PNG)

            if config.video_on_failure and page.video:
                video_path = page.video.path()
                if video_path:
                    allure.attach.file(video_path, name="failure_video", attachment_type=allure.attachment_type.WEBM)

            if config.trace_on_failure:
                trace_path = browser_manager.stop_tracing(test_name)
                allure.attach.file(trace_path, name="failure_trace", attachment_type=allure.attachment_type.ZIP)
    except Exception as e:
        logger.warning(f"Failed to capture failure artifacts: {e}")

    browser_manager.close()


@pytest.fixture
def page(browser_manager: BrowserManager):
    return browser_manager.page


@pytest.fixture
def lm(browser_manager: BrowserManager):
    return browser_manager.locator_manager


@pytest.fixture
def navigate_to(page):
    def _navigate(url: str):
        page.goto(url, wait_until="load")
    return _navigate


@pytest.fixture
def login_as_admin(page, navigate_to):
    def _login():
        navigate_to(f"{config.base_url}/web/login")
        page.wait_for_selector('input[name="login"]', timeout=10000)
        page.fill('input[name="login"]', config.admin_user)
        page.fill('input[name="password"]', config.admin_password)
        page.click('button[type="submit"]')
        page.wait_for_load_state("load")
        assert page.url.startswith(f"{config.base_url}/web"), f"Login failed. Current URL: {page.url}"
    return _login


@pytest.fixture
def performance_metrics(page):
    metrics = {}

    def _start_recording():
        metrics.clear()
        page.on("console", lambda msg: metrics.setdefault("console", []).append(msg.text))

        page.evaluate("""() => {
            window.__perfMarks = {};
            const observer = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    window.__perfMarks[entry.name] = entry;
                }
            });
            observer.observe({ type: 'largest-contentful-paint', buffered: true });
            observer.observe({ type: 'first-input', buffered: true });
            observer.observe({ type: 'layout-shift', buffered: true });
        }""")

    def _get_metrics():
        metrics["lcp"] = page.evaluate("""() => {
            return new Promise((resolve) => {
                new PerformanceObserver((list) => {
                    const entries = list.getEntries();
                    resolve(entries.length > 0 ? entries[entries.length - 1].startTime : null);
                }).observe({ type: 'largest-contentful-paint', buffered: true });
            });
        }""")
        metrics["cls"] = page.evaluate("""() => {
            let cls = 0;
            new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (!entry.hadRecentInput) cls += entry.value;
                }
            }).observe({ type: 'layout-shift', buffered: true });
            return cls;
        }""")
        metrics["page_load"] = page.evaluate("""() => {
            const nav = performance.getEntriesByType('navigation')[0];
            return nav ? nav.loadEventEnd - nav.startTime : null;
        }""")
        return metrics

    def _assert_performance():
        m = _get_metrics()
        if m.get("lcp") and m["lcp"] > config.perf_threshold_lcp:
            logger.warning(f"LCP exceeded threshold: {m['lcp']}ms > {config.perf_threshold_lcp}ms")
        if m.get("cls") and m["cls"] > config.perf_threshold_cls:
            logger.warning(f"CLS exceeded threshold: {m['cls']} > {config.perf_threshold_cls}")
        if m.get("page_load") and m["page_load"] > config.perf_threshold_page_load:
            logger.warning(f"Page load exceeded threshold: {m['page_load']}ms > {config.perf_threshold_page_load}")
        return m

    return {"start_recording": _start_recording, "get_metrics": _get_metrics, "assert_performance": _assert_performance}
