import pygame

from pysim.data.vector import SOUTH, Vector
from pysim.graphics.animations.animation import Animation
from pysim.graphics.primitives.primitive import Primitive
from pysim.gui.mainwindow import MainWindow
from pysim.gui.screen import Screen
from pysim.simulation.events.movement import ForwardEvent


class TestScreen(Screen):
    __animation: Animation[Primitive]
    __total_time: float

    def __init__(self, animation: Animation[Primitive]):
        self.__animation = animation
        self.__total_time = 0

    def update(self, elapsed_seconds: float) -> None:
        self.__total_time += elapsed_seconds

    def render(self, surface: pygame.Surface) -> None:
        self.__clear_screen(surface)
        return self.__animation[self.__total_time].render(surface)

    def __clear_screen(self, surface: pygame.Surface) -> None:
        color = (128, 128, 128)
        surface.fill(color)


def create_animation():
    start = Vector(2, 2)
    direction = SOUTH
    event = ForwardEvent(start, direction)
    return event.animate()


def main():
    pygame.init()
    screen = TestScreen(create_animation())
    window = MainWindow(screen)
    window.run()


if __name__ == '__main__':
    main()
