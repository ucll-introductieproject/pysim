import pygame

from pysim.gui.mainwindow import MainWindow
from pysim.gui.screen import Screen


class TestScreen(Screen):
    def __init__(self):
        pass

    def update(self, elapsed_seconds: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        self.__clear_screen(surface)

    def __clear_screen(self, surface: pygame.Surface) -> None:
        color = (128, 128, 128)
        surface.fill(color)


def main():
    pygame.init()
    screen = TestScreen()
    window = MainWindow(screen)
    window.run()


if __name__ == '__main__':
    main()
