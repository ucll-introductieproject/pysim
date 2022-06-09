from abc import ABC, abstractmethod

from pysim.data import Vector


class Entity(ABC):
    @property
    @abstractmethod
    def position(self) -> Vector:
        ...
