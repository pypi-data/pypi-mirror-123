import dataclasses
from typing import Optional, Dict, Union

MESSAGE_TYPE_ONESHOT = 0
MESSAGE_TYPE_REQUEST = 1
MESSAGE_TYPE_RESPONSE = 2
MESSAGE_TYPE_ERROR = 3
MESSAGE_TYPE_BROADCAST = 4
MESSAGE_TYPE = int
RESPONSE_TYPES = Union['ErrorResponse', 'MessageResponse', 'NotificationResponse']



@dataclasses.dataclass
class Message:
    cmd: str
    type: MESSAGE_TYPE
    param: Optional[Dict] = None
    id: Optional[int] = None


@dataclasses.dataclass
class MessageResponse:
    id: int
    data: str
    type: MESSAGE_TYPE = MESSAGE_TYPE_RESPONSE


@dataclasses.dataclass
class ErrorResponse:
    id: int
    error: str
    type: MESSAGE_TYPE = MESSAGE_TYPE_ERROR


@dataclasses.dataclass
class NotificationResponse:
    cmd: str
    data: str
    type: MESSAGE_TYPE = MESSAGE_TYPE_ONESHOT

