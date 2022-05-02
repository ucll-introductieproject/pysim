from typing import List

from pysim.graphics.animations.animation import Animation
from pysim.graphics.animations.stepwise import StepwiseAnimation
from pysim.graphics.primitives.primitive import Primitive
from pysim.simulation.events.event import Event, AnimationSettings


class EventSequence(Event):
    __children: List[Event]

    def __init__(self, children: List[Event]):
        self.__children = children

    def animate(self, settings: AnimationSettings) -> Animation[Primitive]:
        animations = [c.animate(settings) for c in self.__children]
        return StepwiseAnimation(animations)
