import abc
import json
from abc import ABC
from typing import Any

import kafka
from django.conf import settings

from core.constants.queue import MessageType


class AbstractProducer(ABC):
    def __init__(self):
        self.url = settings.MESSAGE_QUEUE_URL
        self.options = {}
        self.producer = self.connect()

    @abc.abstractmethod
    def connect(self) -> Any:
        pass

    @abc.abstractmethod
    def send(self, message: str, queue_name: str) -> None:
        pass

    def set_options(self, options: dict) -> None:
        self.options = options

    @staticmethod
    def get_message_to_send(data: str, message_type: MessageType) -> str:
        return json.dumps(
            {
                "message_type": message_type,
                "data": data,
            }
        )


class KafkaProducer(AbstractProducer):
    def connect(self) -> kafka.KafkaProducer:
        return kafka.KafkaProducer(bootstrap_servers=self.url)

    def send(self, message: str, queue_name: str) -> None:
        self.producer.send(queue_name, message.encode())
