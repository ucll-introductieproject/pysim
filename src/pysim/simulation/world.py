from __future__ import annotations

from copy import deepcopy
from typing import Any, List

from pysim.data import Grid, Vector
from pysim.simulation.tiles import Tile


class World:
    __grid: Grid[Tile]

    __agent_positions: List[Vector]

    def __init__(self, grid: Grid[Tile], agent_locations: List[Vector]) -> None:
        self.__grid = deepcopy(grid)
        self.__agent_positions = deepcopy(agent_locations)

    @property
    def width(self) -> int:
        return self.__grid.width

    @property
    def height(self) -> int:
        return self.__grid.height

    @property
    def agent_positions(self) -> List[Vector]:
        return self.__agent_positions

    def __getitem__(self, position: Vector) -> Tile:
        return self.__grid[position]

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, World):
            return False
        if self.__grid != other.__grid:
            return False
        if self.__agent_positions != other.__agent_positions:
            return False
        return True

    def __copy__(self) -> World:
        raise NotImplementedError()

    def __deepcopy__(self, memo: Any) -> World:
        # Constructor takes care of deep copying
        return World(self.__grid, self.__agent_positions)
