from typing import List

from pysim.graphics.animations.animation import Animation
from pysim.graphics.graphics_settings import GraphicsSettings
from pysim.graphics.primitives.primitive import Primitive
from pysim.simulation.events.event import Event
from pysim.simulation.events.sequence import EventSequence


class Animator:
    __events: List[Event]
    __context: GraphicsSettings

    def __init__(self, context: GraphicsSettings):
        self.__events = []
        self.__context = context

    def add(self, event: Event) -> None:
        self.__events.append(event)

    def render(self) -> Animation[Primitive]:
        return EventSequence(self.__events).animate(self.__context)
