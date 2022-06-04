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


def changes_state(pairs):
    def wrapper(function):
        return mark.parametrize('start, expected', parsed_pairs)(function)

    parsed_pairs = [(parse_simulation(before), parse_simulation(after)) for before, after in pairs]
    return wrapper


def preserves_state(state_strings):
    def wrapper(function):
        return mark.parametrize('state', parsed)(function)

    parsed = [parse_simulation(s) for s in state_strings]
    return wrapper


@changes_state([
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
def test_forward_into_empty_space(start, expected):
    actual, events = start.forward()
    assert actual.agent == expected.agent


@preserves_state([
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
])
def test_forward_bump_into_wall(state):
    actual, events = state.forward()
    assert actual.agent == state.agent


@changes_state([
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
def test_backward(start, expected):
    actual, events = start.backward()
    assert actual.agent == expected.agent


@preserves_state([
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
def test_backward_bump_into_wall(state):
    actual, events = state.backward()
    assert actual.agent == state.agent


@changes_state([
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
def test_forward_push_block(start, expected):
    actual, event = start.forward()
    assert actual.agent == expected.agent
    assert actual.entities == expected.entities


@changes_state([
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
def test_backward_push_block(start, expected):
    actual, event = start.backward()
    assert actual.agent == expected.agent
    assert actual.entities == expected.entities
