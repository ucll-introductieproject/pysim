from typing import TypeVar, Generic, Callable

from .vector import Vector

T = TypeVar('T')


class Grid(Generic[T]):
    __contents: list[list[T]]

    def __init__(self, width: int, height, initializer: Callable[[Vector], T]):
        assert width >= 1
        assert height >= 1
        self.__contents = [[initializer(Vector(x, y)) for x in range(width)] for y in range(height)]

    def __getitem__(self, position: Vector) -> T:
        assert 0 <= position.x < self.width, f'{position.x} not between 0 and {self.width}'
        assert 0 <= position.y < self.height, f'{position.y} not between 0 and {self.height}'
        return self.__contents[position.y][position.x]

    @property
    def width(self) -> int:
        return len(self.__contents[0])

    @property
    def height(self) -> int:
        return len(self.__contents)
