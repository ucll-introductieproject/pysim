import pygame

from pysim.data import Grid
from pysim.data.mutable_cell import MutableCell
from pysim.data.orientation import NORTH
from pysim.data.vector import Vector
from pysim.graphics.animations.animation import Animation
from pysim.graphics.graphics_settings import GraphicsSettings
from pysim.graphics.primitives.primitive import Primitive
from pysim.gui.mainwindow import MainWindow
from pysim.gui.screen import Screen
from pysim.settings import settings
from pysim.simulation.events.sequence import EventSequence
from pysim.simulation.simulation import Simulation
from pysim.simulation.world import Tile, Wall, Empty, World


class Settings(GraphicsSettings):
    @property
    def tile_size(self) -> float:
        return settings['tile_size']

    def tile_rectangle(self, position: Vector) -> pygame.Rect:
        x, y = position
        left = x * self.tile_size
        top = y * self.tile_size
        width = self.tile_size
        height = self.tile_size
        return pygame.Rect(left, top, width, height)


class TestScreen(Screen):
    __animation: Animation[Primitive]
    __total_time: float
    __world: World

    def __init__(self, world: World, animation: Animation[Primitive]):
        self.__world = world
        self.__animation = animation
        self.__total_time = 0

    def update(self, elapsed_seconds: float) -> None:
        self.__total_time += elapsed_seconds * settings['speedup']

    def render(self, surface: pygame.Surface) -> None:
        TestScreen.__clear_screen(surface)
        self.__render_world(surface)
        return self.__animation[self.__total_time].render(surface)

    @staticmethod
    def __clear_screen(surface: pygame.Surface) -> None:
        color = (128, 128, 128)
        surface.fill(color)

    def __render_world(self, surface: pygame.Surface) -> None:
        self.__world.render(surface, Settings())


def create_world() -> World:
    width = 10
    height = 10
    grid: Grid[MutableCell[Tile]] = Grid(width, height, lambda p: MutableCell[Tile](Empty()))
    grid[Vector(0, 0)].value = Wall()
    world = World(Grid[Tile](width, height, lambda p: grid[p].value))
    return world


def create_animation(world: World):
    start = Vector(2, 2)
    simulation = Simulation(world, start, NORTH)
    settings = Settings()
    events = [
        simulation.forward(),
        simulation.forward(),
        simulation.turn_left(),
        simulation.forward(),
        simulation.forward(),
        simulation.turn_left(),
        simulation.forward(),
        simulation.forward(),
    ]
    return EventSequence(events).animate(settings)


def main():
    pygame.init()
    world = create_world()
    screen = TestScreen(world, create_animation(world))
    window = MainWindow(screen)
    window.run()


if __name__ == '__main__':
    main()
