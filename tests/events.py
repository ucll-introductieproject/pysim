from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pysim.data import Vector
from pysim.simulation.events.eventfactory import EventFactory


class Event(ABC):
    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        ...

    @abstractmethod
    def __hash__(self) -> int:
        ...


class AgentForwardEvent(Event):
    agent_index: int

    def __init__(self, agent_index: int):
        self.agent_index = agent_index

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, AgentForwardEvent) and self.agent_index == other.agent_index

    def __hash__(self) -> int:
        return hash(self.agent_index)


class ObjectMoveEvent(Event):
    origin: Vector
    destination: Vector

    def __init__(self, origin: Vector, destination: Vector):
        self.origin = origin
        self.destination = destination

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ObjectMoveEvent):
            return False
        else:
            return self.origin == other.origin and self.destination == other.destination

    def __hash__(self) -> int:
        return hash(self.origin) ^ hash(self.destination)


class ParallelEvent(Event):
    children: tuple[Event, ...]

    def __init__(self, *children: Event):
        self.children = children

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ParallelEvent) and set(self.children) == set(other.children)

    def __hash__(self) -> int:
        return hash(self.children)


class NothingEvent(Event):
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, NothingEvent)

    def __hash__(self) -> int:
        return 0


class TestEventFactory(EventFactory[Event]):
    def actor_moved_forward(self, agent_index: int) -> Event:
        return AgentForwardEvent(agent_index)

    def object_moved(self, origin: Vector, destination: Vector) -> Event:
        return ObjectMoveEvent(origin, destination)

    def parallel(self, *events: Event) -> Event:
        return ParallelEvent(*events)

    def nothing(self) -> Event:
        return NothingEvent()


def agent_forward(index: int = 0) -> Event:
    return AgentForwardEvent(index)


def object_moved(origin: Vector, destination: Vector) -> Event:
    return ObjectMoveEvent(origin, destination)


def parallel(*children: Event) -> Event:
    return ParallelEvent(*children)


def nothing() -> Event:
    return NothingEvent()
