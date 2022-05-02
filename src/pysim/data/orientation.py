from __future__ import annotations

from abc import abstractmethod, ABC


class Orientation(ABC):
    @abstractmethod
    def turn_left(self) -> Orientation:
        ...

    @abstractmethod
    def turn_right(self) -> Orientation:
        ...

    @abstractmethod
    def turn_around(self) -> Orientation:
        ...

    @property
    @abstractmethod
    def angle(self) -> float:
        ...


class _North(Orientation):
    def turn_left(self) -> Orientation:
        return WEST

    def turn_right(self) -> Orientation:
        return EAST

    def turn_around(self) -> Orientation:
        return SOUTH

    @property
    def angle(self) -> float:
        return 270


class _East(Orientation):
    def turn_left(self) -> Orientation:
        return NORTH

    def turn_right(self) -> Orientation:
        return SOUTH

    def turn_around(self) -> Orientation:
        return WEST

    @property
    def angle(self) -> float:
        return 0


class _South(Orientation):
    def turn_left(self) -> Orientation:
        return EAST

    def turn_right(self) -> Orientation:
        return WEST

    def turn_around(self) -> Orientation:
        return NORTH

    @property
    def angle(self) -> float:
        return 90


class _West(Orientation):
    def turn_left(self) -> Orientation:
        return SOUTH

    def turn_right(self) -> Orientation:
        return NORTH

    def turn_around(self) -> Orientation:
        return EAST

    @property
    def angle(self) -> float:
        return 180


NORTH = _North()
WEST = _West()
SOUTH = _South()
EAST = _East()
