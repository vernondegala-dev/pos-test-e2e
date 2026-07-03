import logging

import allure
import pytest

from src.core.config import config
from src.core.fixtures import *  # noqa: F401, F403
from src.keywords import AuthKeywords, CustomerKeywords, PaymentKeywords, PosKeywords, ProductKeywords
from src.keywords.pos.inventory_keywords import InventoryKeywords
from src.keywords.pos.reporting_keywords import ReportingKeywords
from src.keywords.pos.returns_keywords import ReturnsKeywords
from src.pages.pos import (
    CustomersPage,
    DashboardPage,
    LoginPage,
    OrdersPage,
    PosInterfacePage,
    ProductsPage,
)
from src.pages.pos.inventory_page import InventoryPage
from src.pages.pos.reports_page import ReportsPage
from src.pages.pos.returns_page import ReturnsPage
from src.pages.pos.tax_page import TaxPage
from src.utils.data_generator import DataGenerator

logger = logging.getLogger(__name__)


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def dashboard_page(page):
    return DashboardPage(page)


@pytest.fixture
def pos_interface(page):
    return PosInterfacePage(page)


@pytest.fixture
def products_page(page):
    return ProductsPage(page)


@pytest.fixture
def orders_page(page):
    return OrdersPage(page)


@pytest.fixture
def customers_page(page):
    return CustomersPage(page)


@pytest.fixture
def auth_keywords(login_page, dashboard_page):
    return AuthKeywords(login_page, dashboard_page)


@pytest.fixture
def pos_keywords(pos_interface, orders_page):
    return PosKeywords(pos_interface, orders_page)


@pytest.fixture
def product_keywords(products_page):
    return ProductKeywords(products_page)


@pytest.fixture
def payment_keywords(pos_interface):
    return PaymentKeywords(pos_interface)


@pytest.fixture
def customer_keywords(customers_page):
    return CustomerKeywords(customers_page)


@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)


@pytest.fixture
def returns_page(page):
    return ReturnsPage(page)


@pytest.fixture
def reports_page(page):
    return ReportsPage(page)


@pytest.fixture
def tax_page(page):
    return TaxPage(page)


@pytest.fixture
def inventory_keywords(dashboard_page, inventory_page):
    return InventoryKeywords(dashboard_page, inventory_page)


@pytest.fixture
def returns_keywords(dashboard_page, returns_page):
    return ReturnsKeywords(dashboard_page, returns_page)


@pytest.fixture
def reporting_keywords(dashboard_page, reports_page):
    return ReportingKeywords(dashboard_page, reports_page)


@pytest.fixture
def data_generator():
    return DataGenerator()


@pytest.fixture
def logged_in_admin(auth_keywords):
    auth_keywords.login_as_admin()
    yield auth_keywords
    try:
        if auth_keywords.verify_user_logged_in():
            auth_keywords.logout()
        else:
            logger.info("Already logged out during teardown, skipping.")
    except Exception as e:
        logger.warning(f"Logout during teardown failed: {e}")


@pytest.fixture
def pos_session(logged_in_admin, pos_keywords):
    pos_keywords.open_pos()
    yield pos_keywords
    try:
        pos_keywords.close_pos_session()
    except Exception as e:
        logger.warning(f"POS session teardown failed: {e}")


@pytest.fixture
def started_pos_session(pos_session, pos_interface):
    pos_interface.start_session("100")
    yield pos_session


@pytest.fixture(autouse=True)
def _allure_environment(request):
    allure.dynamic.feature(request.node.get_closest_marker("feature", None).args[0] if request.node.get_closest_marker("feature") else "General")
    allure.dynamic.story(request.node.get_closest_marker("story", None).args[0] if request.node.get_closest_marker("story") else "General")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
