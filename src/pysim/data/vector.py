from __future__ import annotations

import math
from typing import Literal, Iterable


class Vector:
    __x: int
    __y: int

    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    @staticmethod
    def from_polar(angle: Literal[0, 90, 180, 270], radius: int) -> Vector:
        if angle == 0:
            return NORTH * radius
        elif angle == 90:
            return WEST * radius
        elif angle == 180:
            return SOUTH * radius
        elif angle == 270:
            return EAST * radius
        else:
            assert False

    @property
    def angle(self) -> float:
        return math.atan2(self.y, self.x)

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


NORTH: Vector = Vector(0, -1)
EAST: Vector = Vector(1, 0)
SOUTH: Vector = Vector(0, 1)
WEST: Vector = Vector(-1, 0)
