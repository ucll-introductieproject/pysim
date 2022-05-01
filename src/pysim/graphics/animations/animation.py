from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class Animation(ABC, Generic[T]):
    @abstractmethod
    def __getitem__(self, time: float) -> T:
        ...

    @property
    @abstractmethod
    def duration(self) -> float:
        ...
