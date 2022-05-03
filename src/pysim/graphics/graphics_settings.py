from abc import ABC, abstractmethod

from pygame import Rect

from pysim.data import Vector


class GraphicsSettings(ABC):
    @property
    @abstractmethod
    def tile_size(self) -> float:
        ...

    @abstractmethod
    def tile_rectangle(self, position: Vector) -> Rect:
        ...
