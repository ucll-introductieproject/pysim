import pygame

from pysim.graphics.animations.animation import Animation
from pysim.graphics.animations.float import LinearFloatAnimation
from pysim.graphics.primitives.primitive import Primitive
from pysim.graphics.primitives.shapes import Circle
from pysim.gui.mainwindow import MainWindow
from pysim.gui.screen import Screen


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
        self.__animation[self.__total_time].render(surface)

    def __clear_screen(self, surface: pygame.Surface) -> None:
        color = (128, 128, 128)
        surface.fill(color)


def create_animation():
    red = (255, 0, 0)
    return LinearFloatAnimation(100, 200, 1).map(lambda x: Circle(pygame.Vector2(x, x), x / 10, red))


def main():
    pygame.init()
    screen = TestScreen(create_animation())
    window = MainWindow(screen)
    window.run()


if __name__ == '__main__':
    main()
