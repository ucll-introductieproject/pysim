from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List, Dict, Callable

from pytest import mark

import pysim.simulation.objects as objects
import pysim.simulation.tiles as tiles
from events import agent_forward, nothing, parallel, object_moved, TestEventFactory
from pysim.data import Grid, Vector
from pysim.data.orientation import NORTH, EAST, WEST, SOUTH, Orientation
from pysim.simulation.agent import Agent
from pysim.simulation.simulation import Simulation
from pysim.simulation.world import World


class Initializer(ABC):
    grid: Grid[tiles.Tile]
    agents: List[Agent]

    def __init__(self, grid: Grid[tiles.Tile], agents: List[Agent]):
        self.grid = grid
        self.agents = agents

    @abstractmethod
    def initialize(self, position: Vector) -> None:
        ...


TileFactory = Callable[[], tiles.Tile]

ObjectFactory = Callable[[], objects.Object]

InitializerFactory = Callable[[Grid[tiles.Tile], List[Agent]], Initializer]


def tile_initializer_factory(tile_factory: TileFactory) -> InitializerFactory:
    class TileInitializer(Initializer):
        def initialize(self, position: Vector) -> None:
            self.grid[position] = tile_factory()

    return TileInitializer


def object_initializer_factory(object_factory: ObjectFactory) -> InitializerFactory:
    class ObjectInitializer(Initializer):
        def initialize(self, position: Vector) -> None:
            self.grid[position].contents = object_factory()

    return ObjectInitializer


def agent_initializer_factory(orientation: Orientation) -> InitializerFactory:
    class AgentInitializer(Initializer):
        def initialize(self, position: Vector) -> None:
            agent = Agent(position, orientation)
            self.agents.append(agent)

    return AgentInitializer


def combine(*factories: InitializerFactory) -> InitializerFactory:
    class CombinedInitializer(Initializer):
        initializers: List[Initializer]

        def __init__(self, grid: Grid[tiles.Tile], agents: List[Agent]):
            super().__init__(grid, agents)
            self.initializers = [factory(grid, agents) for factory in factories]

        def initialize(self, position: Vector) -> None:
            for initializer in self.initializers:
                initializer.initialize(position)

    return CombinedInitializer


DEFAULT_CHAR_MAP: Dict[str, InitializerFactory] = {
    '.': tile_initializer_factory(tiles.Empty),
    'W': tile_initializer_factory(tiles.Wall),
    'C': tile_initializer_factory(tiles.Chasm),
    '^': combine(tile_initializer_factory(tiles.Empty), agent_initializer_factory(NORTH)),
    'v': combine(tile_initializer_factory(tiles.Empty), agent_initializer_factory(SOUTH)),
    '<': combine(tile_initializer_factory(tiles.Empty), agent_initializer_factory(WEST)),
    '>': combine(tile_initializer_factory(tiles.Empty), agent_initializer_factory(EAST)),
    'B': combine(tile_initializer_factory(tiles.Empty), object_initializer_factory(objects.Block)),
}


def create_parser(factory_map: Dict[str, InitializerFactory]) -> Callable[[List[str]], Simulation]:
    def parse(rows: List[str]) -> Simulation:
        assert len(set(len(row) for row in rows)) == 1, "Rows must be of equal length"
        width = len(rows[0])
        height = len(rows)
        grid = Grid[tiles.Tile](width, height, lambda _: tiles.Empty())
        agents: List[Agent] = []
        initializer_map = {char: factory(grid, agents) for char, factory in factory_map.items()}
        for y, row in enumerate(rows):
            for x, char in enumerate(row):
                position = Vector(x, y)
                initializer_map[char].initialize(position)
        world = World(grid, agents)
        event_factory = TestEventFactory()
        return Simulation(world, event_factory)

    return parse


def changes_state(factory_map: Dict[str, InitializerFactory], triples):
    def wrapper(function):
        return mark.parametrize('state, expected, event', parsed_triples)(function)

    parse = create_parser(factory_map)
    parsed_triples = [(parse(before), parse(after), event) for before, after, event in triples]
    return wrapper


def preserves_state(factory_map: Dict[str, InitializerFactory], state_strings):
    parse = create_parser(factory_map)

    def wrapper(function):
        return mark.parametrize('state', parsed)(function)

    parsed = [parse(s[0]) for s in state_strings]
    return wrapper


@changes_state(
    DEFAULT_CHAR_MAP,
    [
        (
                [
                    '>.',
                ],
                [
                    '.>',
                ],
                agent_forward(),
        ),
        (
                [
                    '.<',
                ],
                [
                    '<.',
                ],
                agent_forward(),
        ),
        (
                [
                    '.',
                    '^',
                ],
                [
                    '^',
                    '.',
                ],
                agent_forward(),
        ),
        (
                [
                    'v',
                    '.',
                ],
                [
                    '.',
                    'v',
                ],
                agent_forward(),
        ),
    ]
)
def test_forward_into_empty_space(state, expected, event):
    e = state.forward(0)
    assert state == expected
    assert event == e


@preserves_state(
    DEFAULT_CHAR_MAP,
    [
        (
                [
                    '>W',
                ],
        ),
        (
                [
                    'W<',
                ],
        ),
        (
                [
                    'W',
                    '^',
                ],
        ),
        (
                [
                    'v',
                    'W',
                ],
        ),
    ]
)
def test_forward_into_wall(state):
    expected = deepcopy(state)
    event = state.forward(0)
    assert state == expected
    assert event == nothing()


@changes_state(
    DEFAULT_CHAR_MAP,
    [
        (
                [
                    '>B.',
                ],
                [
                    '.>B',
                ],
                parallel(
                    agent_forward(),
                    object_moved(Vector(1, 0), EAST)
                ),
        ),
        (
                [
                    '.B<',
                ],
                [
                    'B<.',
                ],
                parallel(
                    agent_forward(),
                    object_moved(Vector(1, 0), WEST)
                ),
        ),
        (
                [
                    'v',
                    'B',
                    '.',
                ],
                [
                    '.',
                    'v',
                    'B',
                ],
                parallel(
                    agent_forward(),
                    object_moved(Vector(0, 1), SOUTH)
                ),
        ),
        (
                [
                    '.',
                    'B',
                    '^',
                ],
                [
                    'B',
                    '^',
                    '.',
                ],
                parallel(
                    agent_forward(),
                    object_moved(Vector(0, 1), NORTH)
                ),
        ),
    ]
)
def test_forward_push_block_to_empty(state, expected, event):
    e = state.forward(0)
    assert state == expected
    assert e == event


@preserves_state(
    DEFAULT_CHAR_MAP,
    [
        (
                [
                    '>BW',
                ],
        ),
        (
                [
                    'WB<',
                ],
        ),
        (
                [
                    'W',
                    'B',
                    '^',
                ],
        ),
        (
                [
                    'v',
                    'B',
                    'W',
                ],
        ),
    ]
)
def test_forward_push_block_into_wall(state):
    expected = deepcopy(state)
    event = state.forward(0)
    assert state == expected
    assert event == nothing()


@preserves_state(
    DEFAULT_CHAR_MAP,
    [
        (
                [
                    '>BB',
                ],
        ),
        (
                [
                    'BB<',
                ],
        ),
        (
                [
                    'B',
                    'B',
                    '^',
                ],
        ),
        (
                [
                    'v',
                    'B',
                    'B',
                ],
        ),
    ]
)
def test_forward_push_block_into_block(state):
    expected = deepcopy(state)
    event = state.forward(0)
    assert state == expected
    assert event == nothing()
