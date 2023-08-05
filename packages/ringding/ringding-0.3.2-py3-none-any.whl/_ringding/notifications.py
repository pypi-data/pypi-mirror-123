import dataclasses
from functools import wraps
from typing import TypeVar

from _ringding.messages import NotificationResponse


RT = TypeVar('RT')  # return type


def notification(notification_id):
    """
    Wrapper to mark a function or class as notification object.

    :param notification_id: The notification id. Clients have to register to this ID
        to react on the incoming notifications.
    :return: A data object that shall be transmitted to the clients.
    """

    def outer_wrap(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            return NotificationResponse(notification_id, func(*args, **kwargs))
        return wrap
    return outer_wrap


@notification('abc.de')
def notify_stuff(x):
    print(x)
    return x


@notification('cde.efg')
@dataclasses.dataclass
class Thing:
    m: int
    n: int
