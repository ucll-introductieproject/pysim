import pygame

from pysim.graphics.animations.animation import Animation
from pysim.graphics.animations.explosion import Explosion
from pysim.graphics.primitives.car import create_car_primitive
from pysim.graphics.primitives.primitive import Primitive
from pysim.gui.mainwindow import MainWindow
from pysim.gui.screen import Screen


class TestScreen(Screen):
    __animation: Animation[Primitive]
    # __car: Primitive
    __total_time: float

    def __init__(self, animation: Animation[Primitive]):
        self.__animation = animation
        # self.__car = create_car_primitive(pygame.Vector2(250, 250), 45, pygame.Color(255, 0, 0), (80, 120))
        self.__total_time = 0

    def update(self, elapsed_seconds: float) -> None:
        self.__total_time += elapsed_seconds

    def render(self, surface: pygame.Surface) -> None:
        self.__clear_screen(surface)
        # self.__car.render(surface)
        create_car_primitive(pygame.Vector2(250, 250), self.__total_time * 90, pygame.Color(255, 0, 0),
                             (80, 120)).render(surface)
        # self.__animation[self.__total_time].render(surface)

    def __clear_screen(self, surface: pygame.Surface) -> None:
        color = (128, 128, 128)
        surface.fill(color)


def create_animation():
    return Explosion(20, pygame.Vector2(200, 200), 2)


def main():
    pygame.init()
    screen = TestScreen(create_animation())
    window = MainWindow(screen)
    window.run()


if __name__ == '__main__':
    main()
