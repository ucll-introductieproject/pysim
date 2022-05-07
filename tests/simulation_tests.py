from typing import List, Optional

from pytest import mark

from pysim.data import Grid, Vector
from pysim.data.orientation import NORTH, EAST, WEST, SOUTH
from pysim.simulation.entities.agent import Agent
from pysim.simulation.entities.block import Block
from pysim.simulation.simulation import Simulation
from pysim.simulation.tiles import Tile, Empty, Wall, Chasm
from pysim.simulation.world import World


def parse_simulation(rows: List[str]) -> Simulation:
    def initialize(position: Vector) -> Tile:
        nonlocal agent
        x, y = position
        match tile := rows[y][x]:
            case '.':
                return Empty()
            case 'W':
                return Wall()
            case 'C':
                return Chasm()
            case 'B':
                entities.append(Block(position))
                return Empty()
            case '^':
                agent = Agent(position, NORTH)
                return Empty()
            case 'v':
                agent = Agent(position, SOUTH)
                return Empty()
            case '<':
                agent = Agent(position, WEST)
                return Empty()
            case '>':
                agent = Agent(position, EAST)
                return Empty()
            case _:
                assert False, f'unparseable {tile}'

    width = len(rows[0])
    height = len(rows)
    agent: Optional[Agent] = None
    entities = []
    world = World(Grid(width, height, initialize))
    assert agent is not None
    return Simulation(world, agent, entities)


@mark.parametrize("str_start, str_end", [
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
])
def test_forward(str_start, str_end):
    start = parse_simulation(str_start)
    expected = parse_simulation(str_end)
    actual, events = start.forward()
    assert actual.agent == expected.agent


@mark.parametrize("str_state", [
    (
            [
                '>W',
            ]
    ),
    (
            [
                'W<',
            ]
    ),
    (
            [
                'v',
                'W',
            ]
    ),
    (
            [
                'W',
                '^',
            ]
    ),
])
def test_forward_bump_into_wall(str_state):
    start = parse_simulation(str_state)
    actual, events = start.forward()
    assert actual.agent == start.agent


@mark.parametrize("str_start, str_end", [
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
])
def test_forward(str_start, str_end):
    start = parse_simulation(str_start)
    expected = parse_simulation(str_end)
    actual, events = start.backward()
    assert actual.agent == expected.agent


@mark.parametrize("str_state", [
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
])
def test_forward_bump_into_wall(str_state):
    start = parse_simulation(str_state)
    actual, events = start.backward()
    assert actual.agent == start.agent


@mark.parametrize("str_start, str_end", [
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
])
def test_push_block(str_start, str_end):
    start = parse_simulation(str_start)
    expected = parse_simulation(str_end)
    actual, event = start.forward()
    assert actual.agent == expected.agent
    assert actual.entities == expected.entities


@mark.parametrize("str_start, str_end", [
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
])
def test_push_block_backward(str_start, str_end):
    start = parse_simulation(str_start)
    expected = parse_simulation(str_end)
    actual, event = start.backward()
    assert actual.agent == expected.agent
    assert actual.entities == expected.entities
