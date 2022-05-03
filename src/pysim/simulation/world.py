from abc import ABC, abstractmethod

from pygame import Rect, Surface, draw

from pysim.data import Grid, Vector
from pysim.graphics.graphics_settings import GraphicsSettings


class Tile(ABC):
    @abstractmethod
    def render(self, surface: Surface, rect: Rect) -> None:
        ...


class Empty(Tile):
    def render(self, surface: Surface, rect: Rect) -> None:
        color = (255, 255, 255)
        draw.rect(surface, color, rect)


class Wall(Tile):
    def render(self, surface: Surface, rect: Rect) -> None:
        color = (64, 64, 64)
        draw.rect(surface, color, rect)


class Chasm(Tile):
    def render(self, surface: Surface, rect: Rect) -> None:
        color = (0, 0, 255)
        draw.rect(surface, color, rect)


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

    def render(self, surface: Surface, settings: GraphicsSettings) -> None:
        for y in range(self.width):
            for x in range(self.height):
                position = Vector(x, y)
                self.__render_tile(surface, settings, position)

    def __render_tile(self, surface: Surface, settings: GraphicsSettings, position: Vector) -> None:
        rect = settings.tile_rectangle(position)
        tile = self[position]
        tile.render(surface, rect)
