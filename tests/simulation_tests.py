from typing import List

from pytest import mark

from pysim.data import Grid, Vector
from pysim.data.orientation import NORTH, EAST, WEST, SOUTH
from pysim.simulation.entities.agent import Agent
from pysim.simulation.simulation import Simulation
from pysim.simulation.tiles import Tile, Empty, Wall, Chasm
from pysim.simulation.world import World


def parse_world(rows: List[str]) -> World:
    def initialize(position: Vector) -> Tile:
        x, y = position
        match tile := rows[y][x]:
            case '.':
                return Empty()
            case 'W':
                return Wall()
            case 'C':
                return Chasm()
            case _:
                assert False, f'unparseable {tile}'

    width = len(rows[0])
    height = len(rows)
    return World(Grid(width, height, initialize))


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
    world = parse_world(world)
    agent = Agent(Vector(*start_position), start_orientation)
    entities = []
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
def test_bump_into_wall(world, start_position, start_orientation):
    world = parse_world(world)
    agent = Agent(Vector(*start_position), start_orientation)
    entities = []
    simulation = Simulation(world, agent, entities)
    result, event = simulation.forward()
    assert result.agent.position == Vector(*start_position)
    assert result.agent.orientation is start_orientation
