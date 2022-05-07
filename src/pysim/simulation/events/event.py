from abc import ABC, abstractmethod

from pysim.graphics.animations.animation import Animation
from pysim.graphics.graphics_settings import GraphicsContext
from pysim.graphics.primitives.primitive import Primitive


class Event(ABC):
    @abstractmethod
    def animate(self, context: GraphicsContext) -> Animation[Primitive]:
        ...
