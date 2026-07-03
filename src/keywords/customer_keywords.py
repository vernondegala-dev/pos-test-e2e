import logging

import allure

from src.pages.pos import CustomersPage

logger = logging.getLogger(__name__)


class CustomerKeywords:
    def __init__(self, customers_page: CustomersPage):
        self.customers_page = customers_page

    @allure.step("Create a new customer: {name}")
    def create_customer(self, name: str, email: str = None, phone: str = None, **kwargs):
        customer_data = {"name": name}
        if email:
            customer_data["email"] = email
        if phone:
            customer_data["phone"] = phone
        customer_data.update(kwargs)

        self.customers_page.create_customer(customer_data)
        assert self.customers_page.customer_exists(name), f"Customer '{name}' was not created"
        logger.info(f"Customer created: {name} ({email})")
        return customer_data

    @allure.step("Delete customer: {name}")
    def delete_customer(self, name: str):
        self.customers_page.delete_customer(name)
        assert not self.customers_page.customer_exists(name), f"Customer '{name}' was not deleted"
        logger.info(f"Customer deleted: {name}")

    @allure.step("Edit customer: {current_name}")
    def edit_customer(self, current_name: str, updates: dict):
        self.customers_page.edit_customer(current_name, updates)
        logger.info(f"Customer updated: {current_name} -> {updates}")
        return updates

    @allure.step("Verify customer exists: {name}")
    def verify_customer_exists(self, name: str) -> bool:
        exists = self.customers_page.customer_exists(name)
        logger.info(f"Customer '{name}' exists: {exists}")
        return exists

    @allure.step("Search customer")
    def search_customer(self, query: str):
        self.customers_page.search_customer(query)
        return self.customers_page

    @allure.step("Create multiple customers")
    def create_multiple_customers(self, customers: list[dict]):
        created = []
        for customer in customers:
            created.append(self.create_customer(**customer))
        return created

    @allure.step("Get customer count")
    def get_customer_count(self) -> int:
        return self.customers_page.get_customer_count()
