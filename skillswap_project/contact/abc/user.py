from abc import abstractmethod


class AbstractUser:
    """Base class for user"""
    @abstractmethod
    @property
    def username() -> str:
        pass

    @abstractmethod
    @property
    def email() -> str:
        pass
