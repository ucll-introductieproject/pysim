from random import Random
from typing import List

from pygame import Vector2

from pysim.graphics.animations.animation import Animation
from pysim.graphics.animations.particle import Particle
from pysim.graphics.primitives.primitive import Primitive
from pysim.graphics.primitives.union import UnionPrimitive


class Explosion(Animation[Primitive]):
    __particles: List[Particle]
    __duration: float

    def __init__(self, n_particles: int, position: Vector2, duration: float):
        def random_particle() -> Particle:
            rnd = Random()
            speed = rnd.uniform(50, 100)
            angle = rnd.uniform(0, 360)
            velocity = Vector2()
            velocity.from_polar((speed, angle))
            size = 24
            r = rnd.randint(220, 255)
            g = rnd.randint(0, 200)
            b = 0
            color = (r, g, b)
            return Particle(position, velocity, size, duration, color)

        self.__duration = duration
        self.__particles = [random_particle() for _ in range(n_particles)]

    @property
    def duration(self):
        return self.duration

    def __getitem__(self, time: float) -> Primitive:
        return UnionPrimitive([p[time] for p in self.__particles])
