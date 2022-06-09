from __future__ import annotations

from typing import Any

from pysim.data import Vector
from pysim.simulation.world import World


class Simulation:
    __world: World

    def __init__(self, world: World) -> None:
        assert world is not None
        self.__world = world

    def forward(self, agent_index: int) -> None:
        agent = self.__world.agents[agent_index]
        destination = agent.position + Vector.from_orientation(agent.orientation)
        tile_at_destination = self.__world[destination]
        if tile_at_destination.is_passable():
            if tile_at_destination.contents is not None:
                object_push_destination = agent.position + Vector.from_orientation(agent.orientation) * 2
                tile_receiving_object = self.__world[object_push_destination]
                if tile_receiving_object.accepts_objects and tile_receiving_object.contents is None:
                    tile_at_destination.contents = None
                    tile_receiving_object.contents = tile_at_destination.contents
                    agent.forward()
            else:
                agent.forward()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Simulation):
            return False
        if self.__world != other.__world:
            return False
        return True
