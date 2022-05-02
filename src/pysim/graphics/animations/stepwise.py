import math
from typing import List, TypeVar

from .animation import Animation

T = TypeVar('T')


class StepwiseAnimation(Animation[T]):
    __children: List[Animation[T]]

    def __init__(self, children: List[Animation[T]]):
        assert children is not None
        self.__children = children

    def __getitem__(self, time: float) -> T:
        step_index = math.floor(time)
        t = time - step_index
        return self.__children[step_index][t]

    @property
    def duration(self) -> float:
        return len(self.__children)
