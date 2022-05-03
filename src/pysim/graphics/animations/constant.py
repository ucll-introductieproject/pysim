from typing import TypeVar

from .animation import Animation

T = TypeVar('T')


class ConstantAnimation(Animation[T]):
    __constant: T
    __duration: float

    def __init__(self, constant: T, duration: float):
        assert duration >= 0

        self.__constant = constant
        self.__duration = duration

    def __getitem__(self, time: float) -> float:
        assert 0 <= time < self.__duration
        return self.__constant

    @property
    def duration(self) -> float:
        return self.__duration
