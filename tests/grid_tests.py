import pytest

from pysim.data import Grid, Vector


@pytest.mark.parametrize("width, height", [(w, h) for w in range(1, 10) for h in range(1, 10)])
def test_size(width, height):
    grid = Grid(width, height, lambda p: None)
    assert grid.width == width
    assert grid.height == height


@pytest.mark.parametrize("width, height", [(w, h) for w in range(1, 10) for h in range(1, 10)])
def test_initialization(width, height):
    def initialize(position: Vector):
        return position.x + position.y * width

    grid = Grid(width, height, initialize)
    index = 0
    for y in range(height):
        for x in range(width):
            p = Vector(x, y)
            assert grid[p] == index
            index += 1
