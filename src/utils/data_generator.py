import random
import string
from datetime import datetime, timedelta
from typing import Optional


class DataGenerator:
    @staticmethod
    def random_string(length: int = 8, prefix: str = "") -> str:
        chars = string.ascii_letters + string.digits
        return f"{prefix}{''.join(random.choices(chars, k=length))}"

    @staticmethod
    def random_email() -> str:
        return f"test.{DataGenerator.random_string(6).lower()}@example.com"

    @staticmethod
    def random_phone() -> str:
        return f"+1{random.randint(200,999)}{random.randint(100,999)}{random.randint(1000,9999)}"

    @staticmethod
    def random_price(min_p: float = 1.0, max_p: float = 999.99) -> float:
        return round(random.uniform(min_p, max_p), 2)

    @staticmethod
    def random_int(min_v: int = 1, max_v: int = 100) -> int:
        return random.randint(min_v, max_v)

    @staticmethod
    def product_data(**overrides) -> dict:
        data = {
            "name": f"Test Product {DataGenerator.random_string(6)}",
            "price": DataGenerator.random_price(),
            "cost": DataGenerator.random_price(0.5, 50),
            "barcode": DataGenerator.random_string(12, "BAR"),
        }
        data.update(overrides)
        return data

    @staticmethod
    def customer_data(**overrides) -> dict:
        data = {
            "name": f"Test Customer {DataGenerator.random_string(6)}",
            "email": DataGenerator.random_email(),
            "phone": DataGenerator.random_phone(),
        }
        data.update(overrides)
        return data

    @staticmethod
    def order_data(product_count: int = 1, **overrides) -> dict:
        products = []
        for _ in range(product_count):
            products.append({
                "name": f"Product {DataGenerator.random_string(4)}",
                "quantity": DataGenerator.random_int(1, 5),
            })
        data = {
            "products": products,
            "payment_method": random.choice(["Cash", "Bank"]),
            "customer": None,
        }
        data.update(overrides)
        return data

    @staticmethod
    def invalid_product_data(**overrides) -> dict:
        data = {
            "name": "",
            "price": -10,
            "barcode": "!@#$%^&*()",
        }
        data.update(overrides)
        return data

    @staticmethod
    def invalid_login_data() -> list:
        return [
            ("", "", "empty credentials"),
            ("invalid_user", "", "no password"),
            ("", "invalid_pass", "no username"),
            ("invalid_user_12345", "wrong_password", "wrong credentials"),
            ("admin", "wrong_password", "wrong password for admin"),
            ("<script>alert('xss')</script>", "password", "XSS injection in username"),
            ("' OR '1'='1", "password", "SQL injection attempt"),
        ]

    @staticmethod
    def bulk_product_data(count: int = 10) -> list:
        return [DataGenerator.product_data() for _ in range(count)]

    @staticmethod
    def bulk_customer_data(count: int = 10) -> list:
        return [DataGenerator.customer_data() for _ in range(count)]

    @staticmethod
    def category_data(**overrides) -> dict:
        data = {
            "name": f"Category {DataGenerator.random_string(6)}",
        }
        data.update(overrides)
        return data
