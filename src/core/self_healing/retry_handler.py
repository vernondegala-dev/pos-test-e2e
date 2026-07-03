import asyncio
import logging
import time
from functools import wraps
from typing import Callable, Optional, Type, Union

from src.core.config import config

logger = logging.getLogger(__name__)


class RetryExhaustedError(Exception):
    pass


def retry_on_failure(
    max_attempts: Optional[int] = None,
    base_delay: Optional[float] = None,
    max_delay: Optional[float] = None,
    exceptions: tuple = (Exception,),
    on_retry: Optional[Callable[[int, Exception], None]] = None,
):
    max_attempts = max_attempts or config.retry_max_attempts
    base_delay = base_delay or config.retry_base_delay
    max_delay = max_delay or config.retry_max_delay

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}: {e}")
                        raise RetryExhaustedError(f"{func.__name__} failed after {max_attempts} attempts") from e
                    delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                    logger.warning(f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}. Retrying in {delay:.1f}s...")
                    if on_retry:
                        on_retry(attempt, e)
                    time.sleep(delay)
            raise RetryExhaustedError(f"{func.__name__} failed after {max_attempts} attempts") from last_exception
        return wrapper
    return decorator


class RetryHandler:
    def __init__(self, max_attempts: int = None, base_delay: float = None, max_delay: float = None):
        self.max_attempts = max_attempts or config.retry_max_attempts
        self.base_delay = base_delay or config.retry_base_delay
        self.max_delay = max_delay or config.retry_max_delay

    def run(self, func: Callable, *args, **kwargs):
        last_exception = None
        for attempt in range(1, self.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt == self.max_attempts:
                    raise RetryExhaustedError(f"Operation failed after {self.max_attempts} attempts") from e
                delay = min(self.base_delay * (2 ** (attempt - 1)), self.max_delay)
                logger.warning(f"Attempt {attempt}/{self.max_attempts} failed. Retrying in {delay:.1f}s...")
                time.sleep(delay)
        raise RetryExhaustedError(f"Operation failed after {self.max_attempts} attempts") from last_exception
