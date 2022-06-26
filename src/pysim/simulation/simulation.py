from __future__ import annotations

from typing import Any

from pysim.simulation.agent import Agent
from pysim.simulation.events import Event
from pysim.simulation.world import World


class Simulation:
    __world: World

    def __init__(self, world: World) -> None:
        assert world is not None
        self.__world = world

    def forward(self, agent_index: int) -> Event:
        agent_position = self.__world.agent_positions[agent_index]
        agent = self.__world[agent_position].contents
        assert isinstance(agent, Agent)
        agent_destination = agent_position.move(agent.orientation)
        destination_tile = self.__world[agent_destination]
        if destination_tile.is_traversable():
            entity = destination_tile.contents
            if entity is not None:
                if entity.is_movable():
                    push_direction = agent.orientation
                    entity_position = agent_destination
                    entity_destination = agent_position.move(agent.orientation, distance=2)
                    tile_receiving_object = self.__world[entity_destination]
                    if tile_receiving_object.accepts_objects:
                        destination_tile.contents = None
                        tile_receiving_object.contents = destination_tile.contents
                        forward_event = agent.forward(agent_position)
                        self.__world.agent_positions[agent_index] = agent_destination
                        move_event = entity.move(entity_position, push_direction)
                        return forward_event.parallel_with(move_event)
                    else:
                        return Event.zero()
                else:
                    return Event.zero()
            else:
                self.__world.agent_positions[agent_index] = agent_destination
                return agent.forward(agent_position)
        else:
            return Event.zero()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Simulation):
            return False
        if self.__world != other.__world:
            return False
        return True
