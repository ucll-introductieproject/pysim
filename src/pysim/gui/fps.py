from abc import ABC

import pygame
from pygame.time import Clock

from pysim.settings import settings


class FpsSource(ABC):
    __clock: Clock

    def __init__(self, clock: Clock):
        self.__clock = clock

    @property
    def fps(self):
        return self.__clock.get_fps()


class Fps:
    __fps_source: FpsSource

    def __init__(self, querier: FpsSource):
        self.__fps_source = querier
        self.__font = pygame.font.SysFont('Comic Sans MS', 30)

    def render(self, surface: pygame.Surface) -> None:
        if settings['show_fps']:
            text = self.__render_fps()
            position = (0, 0)
            surface.blit(text, position)

    def __render_fps(self) -> pygame.surface.Surface:
        fps = self.__fps_source.fps
        antialias = True
        color = (255, 255, 255)
        return self.__font.render(str(fps), antialias, color)
