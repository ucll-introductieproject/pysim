from abc import ABC, abstractmethod

from pysim.data import Vector
from pysim.simulation.events.event import Event


class Entity(ABC):
    @property
    @abstractmethod
    def position(self) -> Vector:
        ...

    @abstractmethod
    def stay(self) -> Event:
        ...
