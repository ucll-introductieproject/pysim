from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict, Callable

from pytest import mark

import pysim.simulation.tiles as tiles
from pysim.data import Grid, Vector
from pysim.data.orientation import NORTH, EAST, WEST, SOUTH, Orientation
from pysim.simulation.entities.agent import Agent
from pysim.simulation.entities.block import Block
from pysim.simulation.entities.entity import Entity
from pysim.simulation.simulation import Simulation
from pysim.simulation.world import World


class Initializer(ABC):
    grid: Grid[tiles.TileState]
    agents: List[Agent]
    entities: List[Entity]

    def __init__(self, grid: Grid[tiles.TileState], agents: List[Agent], entities: List[Entity]):
        self.grid = grid
        self.agents = agents
        self.entities = entities

    @abstractmethod
    def initialize(self, position: Vector) -> None:
        pass


def tile_initializer_factory(tile_factory: Callable[[], tiles.TileState]) -> InitializerFactory:
    class TileInitializer(Initializer):
        def initialize(self, position: Vector) -> None:
            self.grid[position] = tile_factory()

    return TileInitializer


def agent_initializer_factory(orientation: Orientation) -> InitializerFactory:
    class AgentInitializer(Initializer):
        def initialize(self, position: Vector) -> None:
            agent = Agent(position, orientation)
            self.agents.append(agent)

    return AgentInitializer


def entity_initializer_factory(entity_factory: Callable[[Vector], Entity]) -> InitializerFactory:
    class EntityInitializer(Initializer):
        def initialize(self, position: Vector) -> None:
            entity = entity_factory(position)
            self.entities.append(entity)

    return EntityInitializer


def combine(*factories: InitializerFactory) -> InitializerFactory:
    class CombinedInitializer(Initializer):
        initializers: List[Initializer]

        def __init__(self, grid: Grid[tiles.TileState], agents: List[Agent], entities: List[Entity]):
            super().__init__(grid, agents, entities)
            self.initializers = [factory(grid, agents, entities) for factory in factories]

        def initialize(self, position: Vector) -> None:
            for initializer in self.initializers:
                initializer.initialize(position)

    return CombinedInitializer


InitializerFactory = Callable[[Grid[tiles.TileState], List[Agent], List[Entity]], Initializer]

Default: Dict[str, InitializerFactory] = {
    '.': tile_initializer_factory(tiles.Empty),
    'W': tile_initializer_factory(tiles.Wall),
    'C': tile_initializer_factory(tiles.Chasm),
    '^': combine(tile_initializer_factory(tiles.Empty), agent_initializer_factory(NORTH)),
    'v': combine(tile_initializer_factory(tiles.Empty), agent_initializer_factory(SOUTH)),
    '<': combine(tile_initializer_factory(tiles.Empty), agent_initializer_factory(WEST)),
    '>': combine(tile_initializer_factory(tiles.Empty), agent_initializer_factory(EAST)),
    'B': combine(tile_initializer_factory(tiles.Empty), entity_initializer_factory(Block)),
}


def create_parser(factory_map: Dict[str, InitializerFactory]) -> Callable[[List[str]], Simulation]:
    def parse(rows: List[str]) -> Simulation:
        assert len(set(len(row) for row in rows)) == 1, "Rows must be of equal length"
        width = len(rows[0])
        height = len(rows)
        grid = Grid[tiles.TileState](width, height, lambda _: tiles.Empty())
        agents: List[Agent] = []
        entities: List[Entity] = []
        initializer_map = {char: factory(grid, agents, entities) for char, factory in factory_map.items()}
        for y, row in enumerate(rows):
            for x, char in enumerate(row):
                position = Vector(x, y)
                initializer_map[char].initialize(position)
        world = World(grid)
        assert len(agents) == 1, "Only one agent is allowed"
        return Simulation(world, agents[0], entities)

    return parse


def changes_state(factory_map: Dict[str, InitializerFactory], before_after_pairs):
    parse = create_parser(factory_map)

    def wrapper(function):
        return mark.parametrize('start, expected', parsed_pairs)(function)

    parsed_pairs = [(parse(before), parse(after)) for before, after in before_after_pairs]
    return wrapper


def preserves_state(factory_map: Dict[str, InitializerFactory], state_strings):
    parse = create_parser(factory_map)

    def wrapper(function):
        return mark.parametrize('state', parsed)(function)

    parsed = [parse(s) for s in state_strings]
    return wrapper


@changes_state(
    Default,
    [
        (
                [
                    '>.',
                ],
                [
                    '.>',
                ],
        ),
        (
                [
                    '.<',
                ],
                [
                    '<.',
                ],
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
        ),
    ]
)
def test_forward_into_empty_space(start, expected):
    actual, events = start.forward()
    assert actual.agent == expected.agent


@preserves_state(
    Default,
    [
        [
            '>W',
        ],
        [
            'W<',
        ],
        [
            'v',
            'W',
        ],
        [
            'W',
            '^',
        ],
    ]
)
def test_forward_bump_into_wall(state):
    actual, events = state.forward()
    assert actual.agent == state.agent


@changes_state(
    Default,
    [
        (
                [
                    '<.',
                ],
                [
                    '.<',
                ],
        ),
        (
                [
                    '.>',
                ],
                [
                    '>.',
                ],
        ),
        (
                [
                    '.',
                    'v',
                ],
                [
                    'v',
                    '.',
                ],
        ),
        (
                [
                    '^',
                    '.',
                ],
                [
                    '.',
                    '^',
                ],
        ),
    ]
)
def test_backward(start, expected):
    actual, events = start.backward()
    assert actual.agent == expected.agent


@preserves_state(
    Default,
    [
        (
                [
                    '<W',
                ]
        ),
        (
                [
                    'W>',
                ]
        ),
        (
                [
                    '^',
                    'W',
                ]
        ),
        (
                [
                    'W',
                    'v',
                ]
        ),
    ]
)
def test_backward_bump_into_wall(state):
    actual, events = state.backward()
    assert actual.agent == state.agent


@changes_state(
    Default,
    [
        (
                [
                    '>B.',
                ],
                [
                    '.>B',
                ],
        ),
        (
                [
                    '.B<',
                ],
                [
                    'B<.',
                ],
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
        ),
    ]
)
def test_forward_push_block(start, expected):
    actual, event = start.forward()
    assert actual.agent == expected.agent
    assert actual.entities == expected.entities


@changes_state(
    Default,
    [
        (
                [
                    '<B.',
                ],
                [
                    '.<B',
                ],
        ),
        (
                [
                    '.B>',
                ],
                [
                    'B>.',
                ],
        ),
        (
                [
                    '.',
                    'B',
                    'v',
                ],
                [
                    'B',
                    'v',
                    '.',
                ],
        ),
        (
                [
                    '^',
                    'B',
                    '.',
                ],
                [
                    '.',
                    '^',
                    'B',
                ],
        ),
    ]
)
def test_backward_push_block(start, expected):
    actual, event = start.backward()
    assert actual.agent == expected.agent
    assert actual.entities == expected.entities


@changes_state(
    {
        **Default,
        'F': combine(tile_initializer_factory(tiles.Chasm), entity_initializer_factory(Block)),
    },
    [
        (
                [
                    '>F.',
                ],
                [
                    '.F>',
                ],
        ),
        (
                [
                    '.F<',
                ],
                [
                    '<F.',
                ],
        ),
        (
                [
                    'v',
                    'F',
                    '.',
                ],
                [
                    '.',
                    'F',
                    'v',
                ],
        ),
        (
                [
                    '.',
                    'F',
                    '^',
                ],
                [
                    '^',
                    'F',
                    '.',
                ],
        ),
    ]
)
def test_cross_chasm_forward(start, expected):
    state, _ = start.forward()
    actual, _ = state.forward()
    assert actual.agent == expected.agent
    assert actual.entities == expected.entities


@changes_state(
    {
        **Default,
        'F': combine(tile_initializer_factory(tiles.Chasm), entity_initializer_factory(Block)),
    },
    [
        (
                [
                    '.F>',
                ],
                [
                    '>F.',
                ],
        ),
        (
                [
                    '<F.',
                ],
                [
                    '.F<',
                ],
        ),
        (
                [
                    '.',
                    'F',
                    'v',
                ],
                [
                    'v',
                    'F',
                    '.',
                ],
        ),
        (
                [
                    '^',
                    'F',
                    '.',
                ],
                [
                    '.',
                    'F',
                    '^',
                ],
        ),
    ]
)
def test_cross_chasm_backward(start, expected):
    state, _ = start.backward()
    actual, _ = state.backward()
    assert actual.agent == expected.agent
    assert actual.entities == expected.entities
