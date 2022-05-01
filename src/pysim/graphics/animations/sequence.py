from typing import List, TypeVar

from .animation import Animation

T = TypeVar('T')


class SequenceAnimation(Animation[T]):
    __children: List[Animation[T]]

    def __init__(self, children: List[Animation[T]]):
        assert children is not None
        self.__children = children

    def __getitem__(self, time: float) -> T:
        for child in self.__children:
            if time >= child.duration:
                time -= child.duration
            else:
                return child[time]
        assert False

    @property
    def duration(self) -> float:
        return sum(child.duration for child in self.__children)
