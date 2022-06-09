from __future__ import annotations

from typing import Any

from pysim.simulation.world import World


class Simulation:
    __world: World

    def __init__(self, world: World) -> None:
        assert world is not None
        self.__world = world

    def forward(self, agent_index: int) -> None:
        agent = self.__world.agents[agent_index]
        destination = agent.forward_destination()
        tile_at_destination = self.__world[destination]
        if tile_at_destination.is_passable():
            agent.forward()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Simulation):
            return False
        if self.__world != other.__world:
            return False
        return True
