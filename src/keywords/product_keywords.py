import logging

import allure

from src.pages.pos import ProductsPage

logger = logging.getLogger(__name__)


class ProductKeywords:
    def __init__(self, products_page: ProductsPage):
        self.products_page = products_page

    @allure.step("Create a new product: {name}")
    def create_product(self, name: str, price: float, cost: float = None, barcode: str = None, category: str = None):
        product_data = {"name": name, "price": price}
        if cost is not None:
            product_data["cost"] = cost
        if barcode:
            product_data["barcode"] = barcode
        if category:
            product_data["category"] = category

        self.products_page.create_product(product_data)
        assert self.products_page.product_exists(name), f"Product '{name}' was not created"
        logger.info(f"Product created: {name} @ ${price}")
        return product_data

    @allure.step("Update product: {name}")
    def update_product(self, current_name: str, updates: dict):
        self.products_page.edit_product(current_name, updates)
        logger.info(f"Product updated: {current_name} -> {updates}")
        return updates

    @allure.step("Delete product: {name}")
    def delete_product(self, name: str):
        self.products_page.delete_product(name)
        assert not self.products_page.product_exists(name), f"Product '{name}' was not deleted"
        logger.info(f"Product deleted: {name}")

    @allure.step("Verify product exists: {name}")
    def verify_product_exists(self, name: str) -> bool:
        exists = self.products_page.product_exists(name)
        logger.info(f"Product '{name}' exists: {exists}")
        return exists

    @allure.step("Get product count")
    def get_product_count(self) -> int:
        return self.products_page.get_product_count()

    @allure.step("Create multiple products from list")
    def create_multiple_products(self, products: list[dict]):
        created = []
        for product in products:
            created.append(self.create_product(**product))
        return created

    @allure.step("Search product: {query}")
    def search_product(self, query: str):
        self.products_page.search_product(query)
        return self.products_page

    @allure.step("Create product with invalid data expecting failure")
    def create_product_expecting_failure(self, product_data: dict):
        self.products_page.click_create()
        self.products_page.fill_product_form(product_data)
        self.products_page.save()
        has_error = "error" in self.products_page.current_url.lower() or "warning" in self.products_page.current_url.lower()
        assert has_error, "Expected error but product was created successfully"
        logger.info(f"Product creation correctly rejected: {product_data}")
