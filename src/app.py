import pygame

from pysim.graphics.animations.animation import Animation
from pysim.graphics.animations.float import LinearFloatAnimation
from pysim.graphics.layer import Layer
from pysim.graphics.primitives.primitive import Primitive
from pysim.graphics.primitives.shapes import Rectangle
from pysim.gui.mainwindow import MainWindow
from pysim.gui.screen import Screen
from pysim.settings import settings


class TestScreen(Screen):
    __animation: Animation[Primitive]
    __total_time: float
    __layer: Layer

    def __init__(self):
        self.__total_time = 0
        self.__layer = Layer()
        self.__animation = self.__create_animation()

    def __create_animation(self):
        def animate_rectangle(x: float) -> Primitive:
            rect = pygame.Rect(x, 100, 50, 50)
            rectangle = Rectangle(self.__layer, rect, pygame.Color(255, 0, 0))
            return rectangle

        x = LinearFloatAnimation(start=0, stop=1000, duration=10)
        return x.map(animate_rectangle)

    def update(self, elapsed_seconds: float) -> None:
        self.__total_time += elapsed_seconds * settings['speedup']

    def render(self, surface: pygame.Surface) -> None:
        TestScreen.__clear_screen(surface)
        primitive = self.__animation[self.__total_time]
        primitive.render(surface, self.__layer)

    @staticmethod
    def __clear_screen(surface: pygame.Surface) -> None:
        color = (128, 128, 128)
        surface.fill(color)


def main():
    pygame.init()
    screen = TestScreen()
    window = MainWindow(screen)
    window.run()


if __name__ == '__main__':
    main()
