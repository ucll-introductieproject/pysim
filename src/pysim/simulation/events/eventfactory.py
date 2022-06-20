from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from pysim.data import Vector
from pysim.data.orientation import Orientation

Event = TypeVar('Event')


class EventFactory(ABC, Generic[Event]):
    @abstractmethod
    def actor_moved_forward(self, agent_index: int) -> Event:
        ...

    @abstractmethod
    def object_moved(self, origin: Vector, orientation: Orientation) -> Event:
        ...

    @abstractmethod
    def parallel(self, *event: Event) -> Event:
        ...

    @abstractmethod
    def nothing(self) -> Event:
        ...
