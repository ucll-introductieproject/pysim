from __future__ import annotations

from abc import ABC
from typing import Any

from pysim.data import Vector
from pysim.data.orientation import Orientation
from pysim.simulation.entities.entity import Entity
from pysim.simulation.events.event import Event


class _ActorEvent(Event, ABC):
    pass


class _ForwardEvent(_ActorEvent):
    __origin: Vector

    def __init__(self, origin: Vector):
        self.__origin = origin


class _MovedEvent(_ActorEvent):
    __origin: Vector
    __direction: Orientation

    def __init__(self, origin: Vector, direction: Orientation):
        self.__origin = origin
        self.__direction = direction


class Agent(Entity, ABC):
    __orientation: Orientation

    def __init__(self, orientation: Orientation):
        self.__orientation = orientation

    @property
    def orientation(self) -> Orientation:
        return self.__orientation

    def forward(self, origin: Vector) -> Event:
        return _ForwardEvent(origin)

    def is_movable(self) -> bool:
        return True

    def move(self, position: Vector, direction: Orientation) -> Event:
        return _MovedEvent(position, direction)

    # def backward(self) -> None:
    #     self.__position = self.backward_destination()
    #
    # def turn_left(self) -> None:
    #     self.__orientation = self.__orientation.turn_left()
    #
    # def turn_right(self) -> None:
    #     self.__orientation = self.__orientation.turn_right()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Agent) and self.orientation is other.orientation

    def __copy__(self) -> Agent:
        return Agent(self.orientation)

    def __deepcopy__(self, memo: Any) -> Agent:
        return self.__copy__()

    def __str__(self) -> str:
        return f"Agent(orientation={self.orientation})"
