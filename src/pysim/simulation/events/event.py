from __future__ import annotations

from abc import ABC
from functools import reduce
from operator import xor
from typing import Any


class Event(ABC):
    def parallel_with(self, *events: Event):
        return ParallelEvent(tuple([self, *events]))

    @staticmethod
    def zero() -> Event:
        return ZeroOperation()


class ParallelEvent(Event):
    __children: tuple[Event, ...]

    def __init__(self, children: tuple[Event, ...]):
        self.__children = children

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ParallelEvent) and set(self.__children) == set(other.__children)

    def __hash__(self) -> int:
        return reduce(xor, map(hash, self.__children), 0)

    @property
    def children(self) -> tuple[Event, ...]:
        return self.__children


class ZeroOperation(Event):
    def __eq__(self, other) -> bool:
        return isinstance(other, ZeroOperation)

    def __hash__(self) -> int:
        return 0
