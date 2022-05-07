import pygame

from pysim.data import Grid
from pysim.data.mutable_cell import MutableCell
from pysim.data.orientation import NORTH
from pysim.data.vector import Vector
from pysim.graphics.animations.animation import Animation
from pysim.graphics.graphics_settings import GraphicsContext
from pysim.graphics.layer import Layer
from pysim.graphics.primitives.car import create_car
from pysim.graphics.primitives.image import Image
from pysim.graphics.primitives.primitive import Primitive
from pysim.gui.mainwindow import MainWindow
from pysim.gui.screen import Screen
from pysim.settings import settings
from pysim.simulation.animator import Animator
from pysim.simulation.entities.agent import Agent
from pysim.simulation.entities.block import Block
from pysim.simulation.simulation import Simulation
from pysim.simulation.world import Tile, Wall, Empty, World, Chasm


class Context(GraphicsContext):
    __entity_layer: Layer
    __agent_layer: Layer
    __car: Image

    def __init__(self):
        self.__entity_layer = Layer()
        self.__agent_layer = Layer()
        color = pygame.Color(255, 0, 0)
        self.__car = create_car(self.__agent_layer, color, self.tile_size)

    @property
    def entity_layer(self) -> Layer:
        return self.__entity_layer

    @property
    def agent_layer(self) -> Layer:
        return self.__agent_layer

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

    @property
    def agent(self) -> Image:
        return self.__car


class TestScreen(Screen):
    __animation: Animation[Primitive]
    __total_time: float
    __world: World
    __context: GraphicsContext

    def __init__(self, simulation: Simulation, context: GraphicsContext):
        self.__world = simulation.world
        self.__animation = create_animation(context, simulation)
        self.__total_time = 0
        self.__context = context

    def update(self, elapsed_seconds: float) -> None:
        self.__total_time += elapsed_seconds * settings['speedup']

    def render(self, surface: pygame.Surface) -> None:
        TestScreen.__clear_screen(surface)
        self.__render_world(surface)
        primitive = self.__animation[self.__total_time]
        primitive.render(surface, self.__context.entity_layer)
        primitive.render(surface, self.__context.agent_layer)

    @staticmethod
    def __clear_screen(surface: pygame.Surface) -> None:
        color = (128, 128, 128)
        surface.fill(color)

    def __render_world(self, surface: pygame.Surface) -> None:
        self.__world.render(surface, self.__context)


def create_simulation() -> Simulation:
    width = 10
    height = 10
    grid: Grid[MutableCell[Tile]] = Grid(width, height, lambda p: MutableCell[Tile](Empty()))
    grid[Vector(0, 0)].value = Wall()
    grid[Vector(2, 1)].value = Chasm()
    grid[Vector(1, 4)].value = Chasm()
    world = World(Grid[Tile](width, height, lambda p: grid[p].value))
    entities = [
        Block(Vector(1, 3))
    ]
    agent = Agent(Vector(2, 2), NORTH)
    return Simulation(world, agent, entities)


def create_animation(context: GraphicsContext, simulation: Simulation):
    animator = Animator(simulation, context)
    animator.turn_left()
    animator.forward()
    animator.turn_left()
    animator.forward()
    animator.forward()
    return animator.build_animation()


def main():
    pygame.init()
    context = Context()
    simulation = create_simulation()
    screen = TestScreen(simulation, context)
    window = MainWindow(screen)
    window.run()


if __name__ == '__main__':
    main()
