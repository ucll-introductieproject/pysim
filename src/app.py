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
from pysim.simulation.animator import Animator
from pysim.simulation.entities.agent import Agent
from pysim.simulation.entities.block import Block
from pysim.simulation.simulation import Simulation, Simulator
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

    def __init__(self, simulation: Simulation):
        self.__world = simulation.world
        self.__animation = create_animation(simulation)
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


def create_simulation() -> Simulation:
    width = 10
    height = 10
    grid: Grid[MutableCell[Tile]] = Grid(width, height, lambda p: MutableCell[Tile](Empty()))
    grid[Vector(0, 0)].value = Wall()
    world = World(Grid[Tile](width, height, lambda p: grid[p].value))
    entities = [
        Block(Vector(1, 2))
    ]
    agent = Agent(Vector(2, 2), NORTH)
    return Simulation(world, agent, entities)


def create_animation(simulation: Simulation):
    animator = Animator(Settings())
    for event in Simulator(simulation). \
            forward().forward().turn_left().forward().forward().turn_left().forward().forward().events:
        animator.add(event)
    return animator.render()


def main():
    pygame.init()
    simulation = create_simulation()
    screen = TestScreen(simulation)
    window = MainWindow(screen)
    window.run()


if __name__ == '__main__':
    main()
