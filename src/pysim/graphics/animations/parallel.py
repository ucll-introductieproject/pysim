from typing import TypeVar, Callable, Iterable

from .animation import Animation

T = TypeVar('T')
U = TypeVar('U')


class ParallelAnimation(Animation[U]):
    __children: tuple[Animation[T], ...]
    __reducer: Callable[[Iterable[T]], U]

    def __init__(self, reducer: Callable[[Iterable[T]], U], *children: Animation[T]):
        assert len(children) > 0
        self.__children = children
        self.__reducer = reducer

    def __getitem__(self, time: float) -> U:
        return self.__reducer(child[time] for child in self.__children)

    @property
    def duration(self) -> float:
        return min(child.duration for child in self.__children)
