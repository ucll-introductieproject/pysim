from pygame import Surface, Rect, draw

from .tile import Tile


class Wall(Tile):
    def render(self, surface: Surface, rect: Rect) -> None:
        color = (0, 0, 0)
        draw.rect(surface, color, rect)
