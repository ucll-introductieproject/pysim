from typing import TypeVar, Generic, Callable

from .vector import Vector

T = TypeVar('T')


class Grid(Generic[T]):
    __contents: list[list[T]]

    def __init__(self, width: int, height, initializer: Callable[[Vector], T]):
        self.__contents = [[initializer(Vector(x, y)) for x in range(width)] for y in range(height)]

    def __getitem__(self, position: Vector) -> T:
        return self.__contents[position.y][position.x]

    def __setitem__(self, position: Vector, value: T) -> None:
        self.__contents[position.y][position.x] = value

    @property
    def width(self) -> int:
        return len(self.__contents[0])

    @property
    def height(self) -> int:
        return len(self.__contents)
