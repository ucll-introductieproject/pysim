from __future__ import annotations

from typing import Any, TypeVar, Generic

from pysim.data import Vector
from pysim.simulation.events.eventfactory import EventFactory
from pysim.simulation.world import World

Event = TypeVar('Event')


class Simulation(Generic[Event]):
    __world: World
    __event_factory: EventFactory[Event]

    def __init__(self, world: World, event_factory: EventFactory[Event]) -> None:
        assert world is not None
        self.__world = world
        self.__event_factory = event_factory

    def forward(self, agent_index: int) -> Event:
        ef = self.__event_factory
        agent = self.__world.agents[agent_index]
        agent_destination = agent.position + Vector.from_orientation(agent.orientation)
        tile_at_destination = self.__world[agent_destination]
        if tile_at_destination.is_passable():
            if tile_at_destination.contents is not None:
                object_origin = agent_destination
                object_destination = agent.position + Vector.from_orientation(agent.orientation) * 2
                tile_receiving_object = self.__world[object_destination]
                if tile_receiving_object.accepts_objects:
                    tile_at_destination.contents = None
                    tile_receiving_object.contents = tile_at_destination.contents
                    agent.forward()
                    return ef.parallel(
                        ef.actor_moved_forward(agent_index),
                        ef.object_moved(object_origin, object_destination)
                    )
                else:
                    return ef.nothing()
            else:
                agent.forward()
                return ef.actor_moved_forward(agent_index)
        else:
            return ef.nothing()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Simulation):
            return False
        if self.__world != other.__world:
            return False
        return True
