from abc import abstractmethod, ABC
from typing import TYPE_CHECKING
from django.db  import models

if TYPE_CHECKING:
    from typing import Iterable
    from datetime import datetime

class Skill(ABC):
    @abstractmethod
    def name() -> str:
        pass

class Rating(ABC):
    @property
    @abstractmethod
    def rating() -> int:
        pass

    @property
    @abstractmethod
    def rated_at() -> 'datetime':
        pass
    
    @property
    @abstractmethod
    def rated_by() -> 'User':
        pass

    @property
    @abstractmethod
    def skill() -> 'Skill':
        pass

 

class Message(ABC):

    @property
    def message() -> str:
        pass

    @property
    def sender() -> 'User':
        pass

    @property
    def receiver() -> 'User':
        pass


class User(ABC):
    """Base class for user"""
    @property
    @abstractmethod
    def username(self) -> str:
        pass

    @property
    @abstractmethod
    def email(self) -> str:
        pass

    @property
    @abstractmethod
    def full_name(self) -> str:
        pass

    @property
    @abstractmethod
    def skills(self) -> 'Iterable[Skill]':
        pass

    @property
    @abstractmethod
    def ratings() -> 'Iterable[Rating]':
        pass

    @property
    @abstractmethod
    def messages() -> 'Iterable[Message]':
        pass
