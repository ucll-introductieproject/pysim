from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from pysim.data import Vector

Event = TypeVar('Event')


class EventFactory(ABC, Generic[Event]):
    @abstractmethod
    def actor_moved_forward(self, agent_index: int) -> Event:
        ...

    @abstractmethod
    def object_moved(self, origin: Vector, destination: Vector) -> Event:
        ...

    @abstractmethod
    def parallel(self, *event: Event) -> Event:
        ...
