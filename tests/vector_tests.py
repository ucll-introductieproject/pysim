from pysim.data.vector import Vector, NORTH, EAST, SOUTH, WEST
from pytest import mark


@mark.parametrize('x, y', [(x, y) for x in range(-5, 5) for y in range(-5, 5)])
def test_cw_eq_3ccw(x, y):
    vector = Vector(x, y)
    assert vector.rotate_clockwise() == vector.rotate_counterclockwise().rotate_counterclockwise().rotate_counterclockwise()


@mark.parametrize('x, y', [(x, y) for x in range(-5, 5) for y in range(-5, 5)])
def test_3cw_eq_ccw(x, y):
    vector = Vector(x, y)
    assert vector.rotate_clockwise().rotate_clockwise().rotate_clockwise() == vector.rotate_counterclockwise()


@mark.parametrize('x, y', [(x, y) for x in range(-5, 5) for y in range(-5, 5)])
def test_4cw_eq_id(x, y):
    vector = Vector(x, y)
    assert vector.rotate_clockwise().rotate_clockwise().rotate_clockwise().rotate_clockwise() == vector


@mark.parametrize('x, y', [(x, y) for x in range(-5, 5) for y in range(-5, 5)])
def test_4ccw_eq_id(x, y):
    vector = Vector(x, y)
    assert vector.rotate_counterclockwise().rotate_counterclockwise().rotate_counterclockwise().rotate_counterclockwise() == vector


@mark.parametrize('vector, expected', [
    (
        Vector(0, 0),
        Vector(0, 0)
    ),
    (
        NORTH,
        EAST,
    ),
    (
        EAST,
        SOUTH,
    ),
    (
        SOUTH,
        WEST,
    ),
    (
        WEST,
        NORTH,
    ),
    (
        Vector(1, 1),
        Vector(1, -1)
    ),
    (
        Vector(1, -1),
        Vector(-1, -1)
    ),
    (
        Vector(-1, -1),
        Vector(-1, 1)
    ),
    (
        Vector(5, 0),
        Vector(0, -5)
    ),
    (
        Vector(-5, 0),
        Vector(0, 5)
    ),
    (
        Vector(0, 3),
        Vector(3, 0)
    ),
    (
        Vector(0, -3),
        Vector(-3, 0)
    ),
])
def test_cw_rotation(vector, expected):
    actual = vector.rotate_clockwise()
    assert actual == expected