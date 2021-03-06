from abc import ABC, abstractmethod

from pygame import Rect

from pysim.data import Vector
from pysim.graphics.layer import Layer


class GraphicsContext(ABC):
    @property
    @abstractmethod
    def tile_size(self) -> float:
        ...

    @abstractmethod
    def tile_rectangle(self, position: Vector) -> Rect:
        ...

    @property
    @abstractmethod
    def entity_layer(self) -> Layer:
        ...

    @property
    @abstractmethod
    def tile_layer(self) -> Layer:
        ...
