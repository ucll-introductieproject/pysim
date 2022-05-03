from __future__ import annotations

from pysim.data import Vector
from pysim.data.orientation import Orientation


class Agent:
    __position: Vector
    __orientation: Orientation

    def __init__(self, position: Vector, orientation: Orientation):
        self.__position = position
        self.__orientation = orientation

    @property
    def position(self) -> Vector:
        return self.__position

    @property
    def orientation(self) -> Orientation:
        return self.__orientation

    def forward(self) -> Agent:
        direction = Vector.from_orientation(self.__orientation)
        new_position = self.__position + direction
        return Agent(new_position, self.__orientation)

    def backward(self) -> Agent:
        direction = Vector.from_orientation(self.__orientation)
        new_position = self.__position - direction
        return Agent(new_position, self.__orientation)

    def turn_left(self) -> Agent:
        return Agent(self.__position, self.__orientation.turn_left())

    def turn_right(self) -> Agent:
        return Agent(self.__position, self.__orientation.turn_right())
