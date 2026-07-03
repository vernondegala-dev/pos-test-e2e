import logging
from dataclasses import dataclass, field
from typing import Callable, Optional

from playwright.sync_api import FrameLocator, Locator, Page

logger = logging.getLogger(__name__)


class ElementHealingError(Exception):
    pass


@dataclass
class LocatorStrategy:
    name: str
    priority: int
    build: Callable[[Page, dict], Optional[Locator]]
    confidence: float = 1.0


class HealerLocator:
    def __init__(self, page: Page, strategies: list[LocatorStrategy]):
        self._page = page
        self._strategies = sorted(strategies, key=lambda s: s.priority)
        self._resolved_locator: Optional[Locator] = None
        self._resolved_strategy: Optional[str] = None

    @property
    def locator(self) -> Locator:
        if self._resolved_locator and self._is_still_valid():
            return self._resolved_locator
        return self._resolve()

    def _is_still_valid(self) -> bool:
        try:
            self._resolved_locator.element_handle(timeout=1000)
            return True
        except Exception:
            return False

    def _resolve(self) -> Locator:
        for strategy in self._strategies:
            try:
                loc = strategy.build(self._page, {})
                if loc is None:
                    continue
                loc.element_handle(timeout=2000)
                self._resolved_locator = loc
                self._resolved_strategy = strategy.name
                logger.debug(f"Resolved element via strategy: {strategy.name}")
                return loc
            except Exception:
                continue
        raise ElementHealingError("Could not resolve element with any strategy")

    def click(self, **kwargs):
        return self.locator.click(**kwargs)

    def fill(self, value: str, **kwargs):
        return self.locator.fill(value, **kwargs)

    def type(self, text: str, **kwargs):
        return self.locator.type(text, **kwargs)

    def text_content(self, **kwargs) -> Optional[str]:
        return self.locator.text_content(**kwargs)

    def inner_text(self, **kwargs) -> str:
        return self.locator.inner_text(**kwargs)

    def is_visible(self, **kwargs) -> bool:
        return self.locator.is_visible(**kwargs)

    def is_enabled(self, **kwargs) -> bool:
        return self.locator.is_enabled(**kwargs)

    def wait_for(self, **kwargs):
        return self.locator.wait_for(**kwargs)

    def select_option(self, *args, **kwargs):
        return self.locator.select_option(*args, **kwargs)

    def get_attribute(self, name: str, **kwargs) -> Optional[str]:
        return self.locator.get_attribute(name, **kwargs)

    def screenshot(self, **kwargs):
        return self.locator.screenshot(**kwargs)

    def focus(self, **kwargs):
        return self.locator.focus(**kwargs)

    def press(self, key: str, **kwargs):
        return self.locator.press(key, **kwargs)

    def __getattr__(self, name):
        return getattr(self.locator, name)


class LocatorManager:
    def __init__(self, page: Page):
        self._page = page

    def by_testid(self, test_id: str) -> HealerLocator:
        strategies = [
            LocatorStrategy("data-testid", 10, lambda p, _: p.locator(f'[data-testid="{test_id}"]')),
            LocatorStrategy("data-oe-id", 20, lambda p, _: p.locator(f'[data-oe-id="{test_id}"]')),
            LocatorStrategy("id", 30, lambda p, _: p.locator(f'#{test_id}')),
            LocatorStrategy("name", 40, lambda p, _: p.locator(f'[name="{test_id}"]')),
            LocatorStrategy("css-class", 50, lambda p, _: p.locator(f'.{test_id}')),
            LocatorStrategy("xpath-fallback", 100, lambda p, _: p.locator(f'//*[@*[contains(., "{test_id}")]]')),
        ]
        return HealerLocator(self._page, strategies)

    def by_role(self, role: str, name: str = "") -> HealerLocator:
        strategies = [
            LocatorStrategy(f"role-{role}", 10, lambda p, kw: p.get_by_role(role, name=kw.get("name", ""))),
            LocatorStrategy(f"aria-{name}", 30, lambda p, _: p.locator(f'[aria-label*="{name}"]')),
            LocatorStrategy(f"text-{name}", 50, lambda p, _: p.locator(f'text="{name}"')),
        ]
        return HealerLocator(self._page, strategies)

    def by_text(self, text: str, exact: bool = False) -> HealerLocator:
        strategies = [
            LocatorStrategy("text-exact", 10, lambda p, _: p.get_by_text(text, exact=True) if exact else p.get_by_text(text)),
            LocatorStrategy("text-contains", 20, lambda p, _: p.locator(f'text="{text}"')),
            LocatorStrategy("xpath-text", 50, lambda p, _: p.locator(f'//*[contains(text(), "{text}")]')),
        ]
        return HealerLocator(self._page, strategies)

    def by_placeholder(self, placeholder: str) -> HealerLocator:
        strategies = [
            LocatorStrategy("placeholder", 10, lambda p, _: p.get_by_placeholder(placeholder)),
            LocatorStrategy("xpath-placeholder", 30, lambda p, _: p.locator(f'//*[@placeholder="{placeholder}"]')),
        ]
        return HealerLocator(self._page, strategies)

    def by_label(self, label: str) -> HealerLocator:
        strategies = [
            LocatorStrategy("label", 10, lambda p, _: p.get_by_label(label)),
            LocatorStrategy("aria-label", 20, lambda p, _: p.locator(f'[aria-label="{label}"]')),
        ]
        return HealerLocator(self._page, strategies)

    def by_css(self, css: str) -> HealerLocator:
        strategies = [
            LocatorStrategy("css-direct", 10, lambda p, _: p.locator(css)),
            LocatorStrategy("xpath-fallback", 50, lambda p, _: p.locator(f'//*[@class="{css.replace(".", "")}"]')),
        ]
        return HealerLocator(self._page, strategies)

    def by_xpath(self, xpath: str) -> HealerLocator:
        strategies = [
            LocatorStrategy("xpath", 10, lambda p, _: p.locator(xpath)),
        ]
        return HealerLocator(self._page, strategies)
