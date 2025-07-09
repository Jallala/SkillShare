from typing import TYPE_CHECKING
from django.db import models

if TYPE_CHECKING:
    from .abc.user import AbstractUser


class Message:

    @property
    def message() -> str:
        raise NotImplementedError()

    @property
    def sender() -> 'AbstractUser':
        raise NotImplementedError()

    @property
    def receiver() -> 'AbstractUser':
        raise NotImplementedError()
