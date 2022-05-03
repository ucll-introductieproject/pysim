from __future__ import annotations

from typing import List, Tuple

from pysim.simulation.agent import Agent
from pysim.simulation.events.event import Event
from pysim.simulation.events.movement import TurnLeftEvent, ForwardEvent, BackwardEvent, TurnRightEvent, BumpEvent
from pysim.simulation.events.parallel import ParallelEvents
from pysim.simulation.world import World, Wall


class Simulation:
    __world: World
    __agent: Agent

    def __init__(self, world: World, agent: Agent):
        self.__world = world
        self.__agent = agent

    @property
    def world(self) -> World:
        return self.__world

    @property
    def agent(self) -> Agent:
        return self.__agent

    def forward(self) -> Tuple[Simulation, Event]:
        world = self.world
        agent = self.agent
        new_agent = agent.forward()
        destination_tile = world[new_agent.position]
        if isinstance(destination_tile, Wall):
            return (self, BumpEvent(agent.position, agent.orientation))
        else:
            event = ForwardEvent(agent.position, agent.orientation)
            new_state = Simulation(world, new_agent)
            return (new_state, event)

    def backward(self) -> Tuple[Simulation, Event]:
        world = self.world
        agent = self.agent
        new_agent = agent.backward()
        destination_tile = world[new_agent.position]
        if isinstance(destination_tile, Wall):
            return (self, BumpEvent(agent.position, agent.orientation))
        else:
            event = BackwardEvent(agent.position, agent.orientation)
            new_state = Simulation(world, new_agent)
            return (new_state, event)

    def turn_left(self) -> Tuple[Simulation, Event]:
        world = self.world
        agent = self.agent
        new_agent = agent.turn_left()
        new_state = Simulation(world, new_agent)
        event = TurnLeftEvent(agent.position, agent.orientation)
        return (new_state, event)

    def turn_right(self) -> Tuple[Simulation, Event]:
        world = self.world
        agent = self.agent
        new_agent = agent.turn_right()
        new_state = Simulation(world, new_agent)
        event = TurnRightEvent(agent.position, agent.orientation)
        return (new_state, event)

    def __pack_events(self, events: List[Event]) -> Event:
        if len(events) == 1:
            return events[0]
        else:
            return ParallelEvents(events)


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
