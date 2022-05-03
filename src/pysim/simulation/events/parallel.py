from typing import List

from pysim.graphics.animations.animation import Animation
from pysim.graphics.animations.function import FunctionAnimation
from pysim.graphics.graphics_settings import GraphicsSettings
from pysim.graphics.primitives.operations import UnionPrimitive
from pysim.graphics.primitives.primitive import Primitive
from pysim.simulation.events.event import Event


class ParallelEvents(Event):
    __children: List[Event]

    def __init__(self, children: List[Event]):
        self.__children = children

    def animate(self, settings: GraphicsSettings) -> Animation[Primitive]:
        def animate(time: float) -> Primitive:
            return UnionPrimitive([animation[time] for animation in animations])

        animations = [c.animate(settings) for c in self.__children]
        return FunctionAnimation(1, animate)
