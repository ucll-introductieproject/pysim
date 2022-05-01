from pytest import mark

from pysim.data import Vector, NORTH, EAST, SOUTH, WEST


@mark.parametrize('x, y', [(x, y) for x in range(-5, 5) for y in range(-5, 5)])
def test_cw_eq_3ccw(x, y):
    vector = Vector(x, y)
    cw = vector.rotate_clockwise()
    ccw3 = vector.rotate_counterclockwise().rotate_counterclockwise().rotate_counterclockwise()
    assert cw == ccw3


@mark.parametrize('x, y', [(x, y) for x in range(-5, 5) for y in range(-5, 5)])
def test_3cw_eq_ccw(x, y):
    vector = Vector(x, y)
    cw3 = vector.rotate_clockwise().rotate_clockwise().rotate_clockwise()
    ccw = vector.rotate_counterclockwise()
    assert cw3 == ccw


@mark.parametrize('x, y', [(x, y) for x in range(-5, 5) for y in range(-5, 5)])
def test_4cw_eq_id(x, y):
    vector = Vector(x, y)
    cw4 = vector.rotate_clockwise().rotate_clockwise().rotate_clockwise().rotate_clockwise()
    assert cw4 == vector


@mark.parametrize('x, y', [(x, y) for x in range(-5, 5) for y in range(-5, 5)])
def test_4ccw_eq_id(x, y):
    vector = Vector(x, y)
    ccw4 = vector.rotate_counterclockwise().rotate_counterclockwise().rotate_counterclockwise().rotate_counterclockwise()
    assert ccw4 == vector


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