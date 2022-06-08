from typing import Any

from pygame import Surface

from pysim.data import Grid, Vector
from pysim.graphics.graphics_settings import GraphicsContext
from pysim.simulation.tiles import TileState


class World:
    __grid: Grid[TileState]

    def __init__(self, grid: Grid[TileState]):
        self.__grid = grid.shallow_copy()

    @property
    def width(self) -> int:
        return self.__grid.width

    @property
    def height(self) -> int:
        return self.__grid.height

    def __getitem__(self, position: Vector) -> TileState:
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
        return self.__grid == other.__grid
