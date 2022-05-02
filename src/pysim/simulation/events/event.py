from abc import ABC, abstractmethod

from pygame import Rect

from pysim.data import Vector
from pysim.graphics.animations.animation import Animation
from pysim.graphics.primitives.primitive import Primitive


class AnimationSettings(ABC):
    @property
    @abstractmethod
    def tile_size(self) -> float:
        ...

    @abstractmethod
    def tile_rectangle(self, position: Vector) -> Rect:
        ...


class Event(ABC):
    @abstractmethod
    def animate(self, settings: AnimationSettings) -> Animation[Primitive]:
        ...
