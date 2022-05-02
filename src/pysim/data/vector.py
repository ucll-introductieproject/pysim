from __future__ import annotations

from typing import Iterable

from pysim.data.orientation import Orientation, NORTH, WEST, SOUTH, EAST


class Vector:
    __x: int
    __y: int

    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    @staticmethod
    def from_orientation(orientation: Orientation) -> Vector:
        if orientation is NORTH:
            return Vector(0, -1)
        elif orientation is WEST:
            return Vector(-1, 0)
        elif orientation is SOUTH:
            return Vector(0, 1)
        elif orientation is EAST:
            return Vector(1, 0)
        else:
            assert False

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    def rotate_clockwise(self) -> Vector:
        x = self.__y
        y = -self.__x
        return Vector(x, y)

    def rotate_counterclockwise(self) -> Vector:
        x = -self.__y
        y = self.__x
        return Vector(x, y)

    def __add__(self, other: Vector) -> Vector:
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __sub__(self, other: Vector) -> Vector:
        x = self.x - other.x
        y = self.y - other.y
        return Vector(x, y)

    def __mul__(self, factor: int) -> Vector:
        x = self.x * factor
        y = self.y * factor
        return Vector(x, y)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Vector) and self.x == other.x and self.y == other.y

    def __iter__(self) -> Iterable[int]:
        yield self.x
        yield self.y
