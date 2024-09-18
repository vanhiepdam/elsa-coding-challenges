from typing import Iterable

from django.db import OperationalError
from kafka.errors import KafkaTimeoutError
from retrying import retry


def is_connection_issue(error: Exception, exceptions: Iterable) -> bool:
    return any([isinstance(error, exception) for exception in exceptions])


def retry_on_connection_issue(
    retries: int = 3,
    wait_min: int = 1000,
    wait_max: int = 3000,
    exceptions: tuple = (OperationalError, KafkaTimeoutError,),
) -> callable:
    return retry(
        wait_random_min=wait_min,
        wait_random_max=wait_max,
        stop_max_attempt_number=retries,
        retry_on_exception=lambda e: is_connection_issue(e, exceptions),
    )
