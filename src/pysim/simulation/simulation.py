from __future__ import annotations

from typing import List, Tuple, cast

from pysim.data import Vector
from pysim.simulation.entities.agent import Agent, BumpEvent
from pysim.simulation.entities.block import Block
from pysim.simulation.entities.entity import Entity
from pysim.simulation.events.event import Event
from pysim.simulation.events.parallel import ParallelEvents
from pysim.simulation.world import World, Wall


class Simulation:
    __world: World
    __agent: Agent
    __entities: List[Entity]

    def __init__(self, world: World, agent: Agent, entities: List[Entity]):
        self.__world = world
        self.__agent = agent
        self.__entities = entities

    @property
    def world(self) -> World:
        return self.__world

    @property
    def agent(self) -> Agent:
        return self.__agent

    @property
    def entities(self) -> List[Entity]:
        return self.__entities

    def forward(self) -> Tuple[Simulation, Event]:
        world = self.world
        agent = self.agent
        new_agent, agent_event = agent.forward()
        destination = new_agent.position
        if self.__contains_wall(destination):
            bump_event = BumpEvent(agent.position, agent.orientation)
            return (self, bump_event)
        elif self.__contains_block(destination):
            position_beyond_block = agent.position + Vector.from_orientation(agent.orientation) * 2
            if self.__is_free(position_beyond_block):
                block = cast(Block, self.__get_entities_at(destination)[0])
                new_block, block_event = block.move(agent.orientation)
                new_entities = self.__replace_entity(self.__entities, block, new_block)
                new_state = Simulation(world, new_agent, new_entities)
                combined_event = ParallelEvents([agent_event, block_event])
                return (new_state, combined_event)
            else:
                bump_event = BumpEvent(agent.position, agent.orientation)
                return (self, bump_event)
        else:
            new_state = Simulation(world, new_agent, self.__entities)
            return (new_state, agent_event)

    def backward(self) -> Tuple[Simulation, Event]:
        world = self.world
        agent = self.agent
        new_agent, event = agent.backward()
        destination_tile = world[new_agent.position]
        if isinstance(destination_tile, Wall):
            bump_event = BumpEvent(agent.position, agent.orientation)
            return (self, bump_event)
        else:
            new_state = Simulation(world, new_agent, self.__entities)
            return (new_state, event)

    def turn_left(self) -> Tuple[Simulation, Event]:
        world = self.world
        agent = self.agent
        new_agent, event = agent.turn_left()
        new_state = Simulation(world, new_agent, self.__entities)
        return (new_state, event)

    def turn_right(self) -> Tuple[Simulation, Event]:
        world = self.world
        agent = self.agent
        new_agent, event = agent.turn_right()
        new_state = Simulation(world, new_agent, self.__entities)
        return (new_state, event)

    def __pack_events(self, events: List[Event]) -> Event:
        if len(events) == 1:
            return events[0]
        else:
            return ParallelEvents(events)

    def __contains_wall(self, position: Vector) -> bool:
        return isinstance(self.__world[position], Wall)

    def __contains_block(self, position: Vector) -> bool:
        return any(e.position == position and isinstance(e, Block) for e in self.__entities)

    def __is_free(self, position: Vector) -> bool:
        '''
        Checks if there are no entities at the given position
        :param position: Position to check
        :return: True if no objects are present, False otherwise
        '''
        return not any(e.position == position for e in self.__entities)

    def __get_entities_at(self, position: Vector) -> List[Entity]:
        return [e for e in self.__entities if e.position == position]

    def __replace_entity(self, entities: List[Entity], entity: Entity, new_entity: Entity) -> List[Entity]:
        return [
            new_entity,
            *(e for e in self.__entities if e is not entity)
        ]


class Simulator:
    __simulation: Simulation
    __events: List[Event]

    def __init__(self, simulation: Simulation):
        self.__simulation = simulation
        self.__events = []

    @property
    def simulation(self) -> Simulation:
        return self.__simulation

    @property
    def events(self) -> List[Event]:
        return self.__events

    def forward(self) -> Simulator:
        new_state, event = self.__simulation.forward()
        self.__simulation = new_state
        self.__events.append(event)
        return self

    def backward(self) -> Simulator:
        new_state, event = self.__simulation.backward()
        self.__simulation = new_state
        self.__events.append(event)
        return self

    def turn_left(self) -> Simulator:
        new_state, event = self.__simulation.turn_left()
        self.__simulation = new_state
        self.__events.append(event)
        return self

    def turn_right(self) -> Simulator:
        new_state, event = self.__simulation.turn_right()
        self.__simulation = new_state
        self.__events.append(event)
        return self
