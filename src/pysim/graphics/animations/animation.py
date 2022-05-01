from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable

T = TypeVar('T')
U = TypeVar('U')


class Animation(ABC, Generic[T]):
    @abstractmethod
    def __getitem__(self, time: float) -> T:
        ...

    @property
    @abstractmethod
    def duration(self) -> float:
        ...

    def map(self, transformer: Callable[[T], U]) -> Animation[U]:
        return _AnimationMapper[T, U](self, transformer)


class _AnimationMapper(Generic[T, U], Animation[T]):
    __animation: Animation[U]
    __transformer: Callable[[U], T]

    def __init__(self, animation: Animation[U], transformer: Callable[[U], T]):
        self.__animation = animation
        self.__transformer = transformer

    @property
    def duration(self) -> float:
        return self.__animation.duration

    def __getitem__(self, time: float) -> T:
        x = self.__animation[time]
        return self.__transformer(x)
