from __future__ import annotations

from typing import TypeVar, Generic, Callable, Any

from .vector import Vector

T = TypeVar('T')


class Grid(Generic[T]):
    __contents: list[list[T]]

    def __init__(self, width: int, height, initializer: Callable[[Vector], T]):
        assert width >= 1
        assert height >= 1
        self.__contents = [[initializer(Vector(x, y)) for x in range(width)] for y in range(height)]

    def __getitem__(self, position: Vector) -> T:
        assert self.is_inside(position), f'{position} is outside of the grid'
        return self.__contents[position.y][position.x]

    def __setitem__(self, position: Vector, value: T) -> None:
        assert self.is_inside(position), f'{position} is outside of the grid'
        self.__contents[position.y][position.x] = value

    def is_inside(self, position: Vector) -> bool:
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    @property
    def width(self) -> int:
        return len(self.__contents[0])

    @property
    def height(self) -> int:
        return len(self.__contents)

    def shallow_copy(self) -> Grid[T]:
        return Grid(self.width, self.height, self.__getitem__)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Grid):
            return False
        return self.__contents == other.__contents
