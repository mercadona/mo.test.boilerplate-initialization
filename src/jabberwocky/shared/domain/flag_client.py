import abc
from enum import StrEnum


class Flag(StrEnum): ...


class FlagClient(abc.ABC):
    @abc.abstractmethod
    def is_active(self, flag: Flag) -> bool: ...
