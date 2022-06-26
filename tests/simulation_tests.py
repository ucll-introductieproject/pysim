from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List, Dict, Callable, Any

from pytest import mark

import pysim.simulation.entities as entities
import pysim.simulation.tiles as tiles
from pysim.data import Grid, Vector
from pysim.data.orientation import NORTH, EAST, WEST, SOUTH, Orientation
from pysim.simulation.agent import Agent
from pysim.simulation.events import Event
from pysim.simulation.simulation import Simulation
from pysim.simulation.world import World


class Initializer(ABC):
    grid: Grid[tiles.Tile]

    def __init__(self, grid: Grid[tiles.Tile]):
        self.grid = grid

    @abstractmethod
    def initialize(self, position: Vector) -> None:
        ...


TileFactory = Callable[[], tiles.Tile]

EntityFactory = Callable[[], entities.Entity]

TileGrid = Grid[tiles.Tile]

InitializerFactory = Callable[[TileGrid], Initializer]


class TestBlockMovedEvent(Event):
    position: Vector
    direction: Orientation

    def __init__(self, position: Vector, direction: Orientation):
        self.position = position
        self.direction = direction

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, TestBlockMovedEvent):
            return self.position == other.position and self.direction == other.direction
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.position) ^ hash(self.direction)


class TestBlock(entities.Entity):
    # __init__ prevents this class from being identified as a test class
    def __init__(self):
        pass

    def move(self, position: Vector, direction: Orientation) -> Event:
        return TestBlockMovedEvent(position, direction)

    def is_movable(self) -> bool:
        return True

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, TestBlock)


class TestAgentForwardEvent(Event):
    position: Vector

    def __init__(self, position: Vector):
        self.position = position

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, TestAgentForwardEvent) and self.position == other.position

    def __hash__(self) -> int:
        return hash(self.position)


class TestAgent(Agent):
    def __init__(self, orientation: Orientation):
        super().__init__(orientation)

    def forward(self, origin: Vector) -> Event:
        return TestAgentForwardEvent(origin)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, TestAgent)

    def __copy__(self) -> Agent:
        return TestAgent(self.orientation)

    def __deepcopy__(self, memo: Any) -> Agent:
        return self.__copy__()

    def __str__(self) -> str:
        return f"TestAgent(orientation={self.orientation})"


object_moved = TestBlockMovedEvent
agent_forward = TestAgentForwardEvent


def parallel(*events: Event) -> Event:
    return events[0].parallel_with(*events[1:])


def tile_initializer_factory(tile_factory: TileFactory) -> InitializerFactory:
    class TileInitializer(Initializer):
        def initialize(self, position: Vector) -> None:
            self.grid[position] = tile_factory()

    return TileInitializer


def object_initializer_factory(object_factory: EntityFactory) -> InitializerFactory:
    class ObjectInitializer(Initializer):
        def initialize(self, position: Vector) -> None:
            self.grid[position].contents = object_factory()

    return ObjectInitializer


def agent_initializer_factory(orientation: Orientation) -> InitializerFactory:
    class AgentInitializer(Initializer):
        def initialize(self, position: Vector) -> None:
            self.grid[position].contents = TestAgent(orientation)

    return AgentInitializer


def combine(*factories: InitializerFactory) -> InitializerFactory:
    class CombinedInitializer(Initializer):
        initializers: List[Initializer]

        def __init__(self, grid: Grid[tiles.Tile]):
            super().__init__(grid)
            self.initializers = [factory(grid) for factory in factories]

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
    'B': combine(tile_initializer_factory(tiles.Empty), object_initializer_factory(TestBlock)),
}


def create_parser(factory_map: Dict[str, InitializerFactory]) -> Callable[[List[str]], Simulation]:
    def parse(rows: List[str]) -> Simulation:
        assert len(set(len(row) for row in rows)) == 1, "Rows must be of equal length"
        width = len(rows[0])
        height = len(rows)
        grid = Grid[tiles.Tile](width, height, lambda _: tiles.Empty())
        initializer_map = {char: factory(grid) for char, factory in factory_map.items()}
        for y, row in enumerate(rows):
            for x, char in enumerate(row):
                position = Vector(x, y)
                initializer_map[char].initialize(position)
        agent_positions = [position for position in grid.positions if isinstance(grid[position].contents, TestAgent)]
        world = World(grid, agent_positions)
        return Simulation(world)

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
                agent_forward(Vector(0, 0)),
        ),
        (
                [
                    '.<',
                ],
                [
                    '<.',
                ],
                agent_forward(Vector(1, 0)),
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
                agent_forward(Vector(0, 1)),
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
                agent_forward(Vector(0, 0)),
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
    assert event == Event.zero()


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
                    agent_forward(Vector(0, 0)),
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
                    agent_forward(Vector(2, 0)),
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
                    agent_forward(Vector(0, 0)),
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
                    agent_forward(Vector(0, 2)),
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
    assert event == Event.zero()


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
    assert event == Event.zero()
