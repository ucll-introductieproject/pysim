from __future__ import annotations

from copy import deepcopy
from typing import Any, List

from pygame import Surface

from pysim.data import Grid, Vector
from pysim.graphics.graphics_settings import GraphicsContext
from pysim.simulation.entities.agent import Agent
from pysim.simulation.tiles import Tile


class World:
    __grid: Grid[Tile]

    __agents: List[Agent]

    def __init__(self, grid: Grid[Tile], agents: List[Agent]) -> None:
        self.__grid = deepcopy(grid)
        self.__agents = deepcopy(agents)

    @property
    def width(self) -> int:
        return self.__grid.width

    @property
    def height(self) -> int:
        return self.__grid.height

    @property
    def agents(self) -> List[Agent]:
        return self.__agents[:]

    def __getitem__(self, position: Vector) -> Tile:
        return self.__grid[position]

    def render(self, surface: Surface, context: GraphicsContext) -> None:
        for y in range(self.width):
            for x in range(self.height):
                position = Vector(x, y)
                self.__render_tile(surface, context, position)

    def __render_tile(self, surface: Surface, context: GraphicsContext, position: Vector) -> None:
        rect = context.tile_rectangle(position)
        tile = self[position]
        tile.render(surface, rect)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, World):
            return False
        if self.__grid != other.__grid:
            return False
        return True

    def __copy__(self) -> World:
        raise NotImplementedError()

    def __deepcopy__(self, memodict: Any) -> World:
        # Constructor takes care of deep copying
        return World(self.__grid, self.__agents)
