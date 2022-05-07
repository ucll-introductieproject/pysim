from pygame import Rect, Surface, draw

from .tile import Tile


class Chasm(Tile):
    def render(self, surface: Surface, rect: Rect) -> None:
        color = (0, 0, 255)
        draw.rect(surface, color, rect)
