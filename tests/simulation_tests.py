from typing import List, Tuple

from pytest import mark

from pysim.data import Grid, Vector
from pysim.data.orientation import NORTH, EAST, WEST, SOUTH
from pysim.simulation.entities.agent import Agent
from pysim.simulation.entities.block import Block
from pysim.simulation.entities.entity import Entity
from pysim.simulation.simulation import Simulation
from pysim.simulation.tiles import Tile, Empty, Wall, Chasm
from pysim.simulation.world import World


def parse_world(rows: List[str]) -> Tuple[World, List[Entity]]:
    def initialize(position: Vector) -> Tile:
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
            case _:
                assert False, f'unparseable {tile}'

    width = len(rows[0])
    height = len(rows)
    entities = []
    world = World(Grid(width, height, initialize))
    return (world, entities)


@mark.parametrize("world, start_position, start_orientation, end_position", [
    (
            [
                '..',
            ],
            (0, 0),
            EAST,
            (1, 0)
    ),
    (
            [
                '..',
            ],
            (1, 0),
            WEST,
            (0, 0)
    ),
    (
            [
                '.',
                '.',
            ],
            (0, 0),
            SOUTH,
            (0, 1)
    ),
    (
            [
                '.',
                '.',
            ],
            (0, 1),
            NORTH,
            (0, 0)
    ),
])
def test_forward(world, start_position, start_orientation, end_position):
    world, entities = parse_world(world)
    agent = Agent(Vector(*start_position), start_orientation)
    simulation = Simulation(world, agent, entities)
    result, event = simulation.forward()
    assert result.agent.position == Vector(*end_position)
    assert result.agent.orientation is start_orientation


@mark.parametrize("world, start_position, start_orientation", [
    (
            [
                '.W',
            ],
            (0, 0),
            EAST,
    ),
    (
            [
                'W.',
            ],
            (1, 0),
            WEST,
    ),
    (
            [
                '.',
                'W',
            ],
            (0, 0),
            SOUTH,
    ),
    (
            [
                'W',
                '.',
            ],
            (0, 1),
            NORTH,
    ),
])
def test_forward_bump_into_wall(world, start_position, start_orientation):
    world, entities = parse_world(world)
    agent = Agent(Vector(*start_position), start_orientation)
    simulation = Simulation(world, agent, entities)
    result, event = simulation.forward()
    assert result.agent.position == Vector(*start_position)
    assert result.agent.orientation is start_orientation


@mark.parametrize("world, start_position, start_orientation, end_position", [
    (
            [
                '..',
            ],
            (1, 0),
            EAST,
            (0, 0)
    ),
    (
            [
                '..',
            ],
            (0, 0),
            WEST,
            (1, 0)
    ),
    (
            [
                '.',
                '.',
            ],
            (0, 1),
            SOUTH,
            (0, 0)
    ),
    (
            [
                '.',
                '.',
            ],
            (0, 0),
            NORTH,
            (0, 1)
    ),
])
def test_backward(world, start_position, start_orientation, end_position):
    world, entities = parse_world(world)
    agent = Agent(Vector(*start_position), start_orientation)
    simulation = Simulation(world, agent, entities)
    result, event = simulation.backward()
    assert result.agent.position == Vector(*end_position)
    assert result.agent.orientation is start_orientation


@mark.parametrize("world, start_position, start_orientation", [
    (
            [
                '.W',
            ],
            (0, 0),
            WEST,
    ),
    (
            [
                'W.',
            ],
            (1, 0),
            EAST,
    ),
    (
            [
                '.',
                'W',
            ],
            (0, 0),
            NORTH,
    ),
    (
            [
                'W',
                '.',
            ],
            (0, 1),
            SOUTH,
    ),
])
def test_backward_bump_into_wall(world, start_position, start_orientation):
    world, entities = parse_world(world)
    agent = Agent(Vector(*start_position), start_orientation)
    simulation = Simulation(world, agent, entities)
    result, event = simulation.backward()
    assert result.agent.position == Vector(*start_position)
    assert result.agent.orientation is start_orientation


@mark.parametrize("world, start_position, start_orientation, new_world", [
    (
            [
                '.B.',
            ],
            (0, 0),
            EAST,
            [
                '..B',
            ],
    ),
    (
            [
                '.B.',
            ],
            (2, 0),
            WEST,
            [
                'B..',
            ],
    ),
    (
            [
                '.',
                'B',
                '.',
            ],
            (0, 0),
            SOUTH,
            [
                '.',
                '.',
                'B',
            ],
    ),
    (
            [
                '.',
                'B',
                '.',
            ],
            (0, 2),
            NORTH,
            [
                'B',
                '.',
                '.',
            ],
    ),
])
def test_push_block(world, start_position, start_orientation, new_world):
    world, entities = parse_world(world)
    new_world, new_entities = parse_world(new_world)
    agent = Agent(Vector(*start_position), start_orientation)
    simulation = Simulation(world, agent, entities)
    result, event = simulation.forward()
    assert result.entities == new_entities
