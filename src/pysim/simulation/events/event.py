from abc import ABC, abstractmethod

from pysim.graphics.animations.animation import Animation
from pysim.graphics.graphics_settings import GraphicsSettings
from pysim.graphics.primitives.primitive import Primitive


class Event(ABC):
    @abstractmethod
    def animate(self, settings: GraphicsSettings) -> Animation[Primitive]:
        ...
