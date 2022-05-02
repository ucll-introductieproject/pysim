from abc import ABC

from pysim.data import Grid, Vector


class Tile(ABC):
    pass


class Empty(Tile):
    pass


class Wall(Tile):
    pass


class World:
    __grid: Grid[Tile]

    def __init__(self, grid: Grid[Tile]):
        self.__grid = grid

    @property
    def width(self) -> int:
        return self.__grid.width

    @property
    def height(self) -> int:
        return self.__grid.height

    def __getitem__(self, position: Vector) -> Tile:
        return self.__grid[position]
