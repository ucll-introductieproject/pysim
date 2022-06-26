from abc import ABC, abstractmethod

from pysim.data import Vector
from pysim.data.orientation import Orientation
from pysim.simulation.events import Event


class Entity(ABC):
    @abstractmethod
    def is_movable(self) -> bool:
        ...

    @abstractmethod
    def move(self, position: Vector, direction: Orientation) -> Event:
        ...
