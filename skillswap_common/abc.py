from abc import abstractmethod, ABC
from typing import TYPE_CHECKING
from django.db import models

if TYPE_CHECKING:
    from typing import Iterable, TypeAlias, Literal
    from datetime import datetime
    from django.contrib.auth.base_user import AbstractBaseUser
    User: TypeAlias = 'UserProfile | AbstractBaseUser'
    SkillType: TypeAlias = Literal['O'] | Literal['R']


class SkillCategory(ABC):
    @property
    @abstractmethod
    def name(self) -> 'str':
        pass


class Skill(ABC):
    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def user(self) -> 'User':
        pass

    @property
    @abstractmethod
    def title(self) -> 'str':
        pass

    @property
    @abstractmethod
    def description(self) -> 'str':
        pass

    @property
    @abstractmethod
    def availability(self) -> 'bool':
        pass

    @property
    @abstractmethod
    def location(self) -> 'str':
        pass

    @property
    @abstractmethod
    def skill_type(self) -> 'SkillType':
        pass

    @property
    @abstractmethod
    def skill_categroy(self) -> 'SkillCategory':
        pass


class Rating(ABC):
    @property
    @abstractmethod
    def rating(self) -> int:
        pass

    @property
    @abstractmethod
    def rated_at(self) -> 'datetime':
        pass

    @property
    @abstractmethod
    def rated_by(self) -> 'User':
        pass

    @property
    @abstractmethod
    def skill(self) -> 'Skill':
        pass


class Message(ABC):

    @property
    def message(self) -> str:
        pass

    @property
    def sender(self) -> 'User':
        pass

    @property
    def receiver(self) -> 'User':
        pass


class UserProfile(ABC):
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
