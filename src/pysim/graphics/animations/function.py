from typing import TypeVar, Callable

from .animation import Animation

T = TypeVar('T')


class FunctionAnimation(Animation[T]):
    __function: Callable[[float], T]
    __duration: float

    def __init__(self, duration: float, function: Callable[[float], T]):
        self.__function = function
        self.__duration = duration

    def __getitem__(self, time: float) -> T:
        assert 0 <= time < self.__duration
        return self.__function(time)

    @property
    def duration(self) -> float:
        return self.__duration
