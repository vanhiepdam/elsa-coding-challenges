from enum import Enum


class QueueName(str, Enum):
    LEADERBOARD = "leaderboard"


class MessageType(str, Enum):
    LEADERBOARD_UPDATE = "leaderboard_update"
