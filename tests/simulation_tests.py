from pysim.data import Grid, Vector
from pysim.data.orientation import NORTH, EAST
from pysim.simulation.entities.agent import Agent
from pysim.simulation.simulation import Simulation
from pysim.simulation.tiles import Tile, Empty, Wall, Chasm
from pysim.simulation.world import World


def parse_world(s: str) -> World:
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

    rows = [row.strip() for row in s.strip().split("\n")]
    width = len(rows[0])
    height = len(rows)
    return World(Grid(width, height, initialize))


def test_forward_east():
    world = parse_world('''
    ..
    ''')
    agent = Agent(Vector(0, 0), EAST)
    entities = []
    simulation = Simulation(world, agent, entities)
    result, event = simulation.forward()
    assert result.agent.position == Vector(1, 0)
    assert result.agent.orientation is EAST


def test_forward_north():
    world = parse_world('''
        .
        .
        ''')
    agent = Agent(Vector(0, 1), NORTH)
    entities = []
    simulation = Simulation(world, agent, entities)
    result, event = simulation.forward()
    assert result.agent.position == Vector(0, 0)
    assert result.agent.orientation is NORTH
