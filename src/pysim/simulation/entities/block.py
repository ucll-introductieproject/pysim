from pysim.data import Vector
from pysim.data.orientation import Orientation
from pysim.simulation.entities.entity import Entity
from pysim.simulation.events.event import Event


class _MovedEvent(Event):
    __position: Vector
    __direction: Orientation

    def __init__(self, position: Vector, direction: Orientation):
        self.__position = position
        self.__direction = direction


class Block(Entity):
    def move(self, position: Vector, direction: Orientation) -> Event:
        return _MovedEvent(position, direction)

    def is_movable(self) -> bool:
        return True
