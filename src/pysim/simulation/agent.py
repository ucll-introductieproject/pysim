from __future__ import annotations

from typing import Any

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

    def forward_destination(self) -> Vector:
        """
        Returns the position of the agent were it to move forward.
        """
        return self.position + Vector.from_orientation(self.orientation)

    def forward(self) -> None:
        self.__position = self.forward_destination()

    def backward_destination(self) -> Vector:
        """
        Returns the position of the agent were it to move backward.
        """
        return self.position - Vector.from_orientation(self.orientation)

    def backward(self) -> None:
        self.__position = self.backward_destination()

    def turn_left(self) -> None:
        self.__orientation = self.__orientation.turn_left()

    def turn_right(self) -> None:
        self.__orientation = self.__orientation.turn_right()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Agent) and self.position == other.position and self.orientation is other.orientation

    def __copy__(self) -> Agent:
        return Agent(self.position, self.orientation)

    def __deepcopy__(self, memodict: Any) -> Agent:
        return self.__copy__()

    def __str__(self) -> str:
        return f"Agent({self.position}, {self.orientation})"
