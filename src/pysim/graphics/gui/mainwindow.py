from typing import cast

import pygame

from pysim.settings import settings
from .fps import Fps, FpsSource
from .screen import Screen


class MainWindow:
    __surface: pygame.Surface
    __clock: pygame.time.Clock
    __screen: Screen
    __fps: Fps

    def __init__(self, initial_screen: Screen):
        size = (1920, 1080)
        self.__surface = cast(pygame.Surface, pygame.display.set_mode(size))
        self.__clock = pygame.time.Clock()
        self.__screen = initial_screen
        self.__fps = Fps(FpsSource(self.__clock))

    @property
    def screen(self) -> Screen:
        return self.__screen

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    key = event.key
                    ctrl = (event.mod & pygame.KMOD_CTRL) != 0

                    if key == pygame.K_f and ctrl:
                        settings['show_fps'] = not settings['show_fps']

            elapsed_seconds = self.__get_elapsed_seconds()

            self.screen.update(elapsed_seconds)
            self.screen.render(self.__surface)
            self.__fps.render(self.__surface)

            pygame.display.flip()

    def __get_elapsed_seconds(self):
        max_fps = settings['max_fps']
        return self.__clock.tick(max_fps) / 1000

    @property
    def fps(self):
        return self.__clock.get_fps()
