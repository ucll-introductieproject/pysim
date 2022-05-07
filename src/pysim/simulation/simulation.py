from __future__ import annotations

from typing import List, Tuple, cast, Type

from pysim.data import Vector
from pysim.data.orientation import Orientation
from pysim.simulation.entities.agent import Agent, BumpEvent
from pysim.simulation.entities.block import Block
from pysim.simulation.entities.entity import Entity
from pysim.simulation.events.event import Event
from pysim.simulation.events.parallel import ParallelEvents
from pysim.simulation.tiles import Chasm, Empty, Wall, match_tile
from pysim.simulation.world import World


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
        def to_empty():
            world = self.__world
            if self.__contains_block(destination):
                if self.__can_push_block(destination, agent.orientation):
                    entity_at_position, other_entities = self.__extract_entity_at(destination)
                    block = cast(Block, entity_at_position)
                    new_block, block_event = block.move(agent.orientation)
                    new_entities = [new_block, *other_entities]
                    new_state = Simulation(world, new_agent, new_entities)
                    other_entity_events = [e.stay() for e in other_entities]
                    combined_event = ParallelEvents([agent_event, block_event, *other_entity_events])
                    return (new_state, combined_event)
                else:
                    return self.__bump()
            else:
                return self.___move_forward_unhindered()

        def to_wall():
            return self.__bump()

        def to_chasm():
            if self.__contains_block(destination):
                return self.___move_forward_unhindered()
            else:
                return self.__forward_to_wall()

        agent = self.agent
        new_agent, agent_event = agent.forward()
        destination = new_agent.position
        destination_tile = self.__world[destination]
        return match_tile(
            destination_tile,
            if_empty=to_empty,
            if_wall=to_wall,
            if_chasm=to_chasm)

    def __forward_to_chasm(self) -> Tuple[Simulation, Event]:
        agent = self.agent
        new_agent, agent_event = agent.forward()
        destination = new_agent.position
        if self.__contains_block(destination):
            return self.___move_forward_unhindered()
        else:
            return self.__forward_to_wall()

    def __forward_to_wall(self) -> Tuple[Simulation, Event]:
        return self.__bump()

    def __forward_to_empty(self) -> Tuple[Simulation, Event]:
        agent = self.agent
        new_agent, agent_event = agent.forward()
        destination = new_agent.position
        world = self.__world
        if self.__contains_block(destination):
            if self.__can_push_block(destination, agent.orientation):
                entity_at_position, other_entities = self.__extract_entity_at(destination)
                block = cast(Block, entity_at_position)
                new_block, block_event = block.move(agent.orientation)
                new_entities = [new_block, *other_entities]
                new_state = Simulation(world, new_agent, new_entities)
                other_entity_events = [e.stay() for e in other_entities]
                combined_event = ParallelEvents([agent_event, block_event, *other_entity_events])
                return (new_state, combined_event)
            else:
                return self.__bump()
        else:
            return self.___move_forward_unhindered()

    def ___move_forward_unhindered(self) -> Tuple[Simulation, Event]:
        agent = self.agent
        new_agent, agent_event = agent.forward()
        world = self.__world
        new_state = Simulation(world, new_agent, self.__entities)
        entity_events = [e.stay() for e in self.__entities]
        packed = self.__pack_events([agent_event, *entity_events])
        return (new_state, packed)

    def __can_push_block(self, block_position: Vector, orientation: Orientation) -> bool:
        position_beyond_block = block_position.move(orientation)
        if self.__contains_wall(position_beyond_block):
            return False
        return self.__is_free(position_beyond_block)

    def __bump(self) -> Tuple[Simulation, Event]:
        agent = self.agent
        bump_event = BumpEvent(agent.position, agent.orientation)
        entity_events = [e.stay() for e in self.__entities]
        packed = self.__pack_events([bump_event, *entity_events])
        return (self, packed)

    def backward(self) -> Tuple[Simulation, Event]:
        world = self.world
        agent = self.agent
        new_agent, agent_event = agent.backward()
        destination = new_agent.position
        if self.__contains_wall(destination):
            bump_event = BumpEvent(agent.position, agent.orientation)
            entity_events = [e.stay() for e in self.__entities]
            packed = self.__pack_events([bump_event, *entity_events])
            return (self, packed)
        elif self.__contains_block(destination):
            position_beyond_block = agent.position - Vector.from_orientation(agent.orientation) * 2
            if self.__is_free(position_beyond_block):
                entity_at_position, other_entities = self.__extract_entity_at(destination)
                block = cast(Block, entity_at_position)
                new_block, block_event = block.move(agent.orientation.turn_around())
                new_entities = [new_block, *other_entities]
                new_state = Simulation(world, new_agent, new_entities)
                other_entity_events = [e.stay() for e in other_entities]
                combined_event = ParallelEvents([agent_event, block_event, *other_entity_events])
                return (new_state, combined_event)
            else:
                bump_event = BumpEvent(agent.position, agent.orientation)
                entity_events = [e.stay() for e in self.__entities]
                packed = self.__pack_events([bump_event, *entity_events])
                return (self, packed)
        else:
            new_state = Simulation(world, new_agent, self.__entities)
            entity_events = [e.stay() for e in self.__entities]
            packed = self.__pack_events([agent_event, *entity_events])
            return (new_state, packed)

    def turn_left(self) -> Tuple[Simulation, Event]:
        world = self.world
        agent = self.agent
        new_agent, event = agent.turn_left()
        new_state = Simulation(world, new_agent, self.__entities)
        entity_events = [e.stay() for e in self.__entities]
        packed = self.__pack_events([event, *entity_events])
        return (new_state, packed)

    def turn_right(self) -> Tuple[Simulation, Event]:
        world = self.world
        agent = self.agent
        new_agent, event = agent.turn_right()
        new_state = Simulation(world, new_agent, self.__entities)
        entity_events = [e.stay() for e in self.__entities]
        packed = self.__pack_events([event, *entity_events])
        return (new_state, packed)

    def __pack_events(self, events: List[Event]) -> Event:
        if len(events) == 1:
            return events[0]
        else:
            return ParallelEvents(events)

    def __contains_tile_of_type(self, position: Vector, tile_type: Type):
        return isinstance(self.__world[position], tile_type)

    def __contains_empty(self, position: Vector) -> bool:
        return self.__contains_tile_of_type(position, Empty)

    def __contains_wall(self, position: Vector) -> bool:
        return self.__contains_tile_of_type(position, Wall)

    def __contains_chasm(self, position: Vector) -> bool:
        return self.__contains_tile_of_type(position, Chasm)

    def __contains_block(self, position: Vector) -> bool:
        return any(e.position == position and isinstance(e, Block) for e in self.__entities)

    def __is_free(self, position: Vector) -> bool:
        """
        Checks if there are no entities at the given position
        :param position: Position to check
        :return: True if no objects are present, False otherwise
        """
        return not any(e.position == position for e in self.__entities)

    def __get_entities_at(self, position: Vector) -> List[Entity]:
        return [e for e in self.__entities if e.position == position]

    def __extract_entity_at(self, position: Vector) -> Tuple[Entity, List[Entity]]:
        at_position: List[Entity] = []
        rest: List[Entity] = []
        for entity in self.__entities:
            if entity.position == position:
                at_position.append(entity)
            else:
                rest.append(entity)
        assert len(at_position) == 1
        return (at_position[0], rest)

    def __replace_entity(self, entities: List[Entity], entity: Entity, new_entity: Entity) -> List[Entity]:
        return [
            new_entity,
            *(e for e in entities if e is not entity)
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
