from unittest.mock import Mock

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    client = APIClient()
    return client


@pytest.fixture(autouse=True)
def mock_redis_lock(mocker):
    mocker.patch(
        "core.utils.cache.RedisClient.__init__",
        return_value=None,
    )
    mocker.patch(
        "core.utils.cache.RedisLock.__init__",
        return_value=None,
    )
    mocker.patch(
        "core.utils.cache.RedisLock.__enter__",
        return_value=None,
    )
    mocker.patch(
        "core.utils.cache.RedisLock.__exit__",
        return_value=None,
    )


@pytest.fixture(autouse=True)
def mock_kafka_producer(mocker):
    mocker.patch(
        "core.utils.message_queue.KafkaProducer.connect",
        return_value=Mock(send=lambda *args, **kwargs: None),
    )
