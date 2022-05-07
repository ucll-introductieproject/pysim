from math import ulp

from pytest import approx
from pytest import mark

from pysim.graphics.animations.float import LinearFloatAnimation


def almost(n):
    return n - ulp(n)


@mark.parametrize("start, stop, duration",
                  [(start, stop, duration)
                   for start in [0, 1, 4, 17, 201]
                   for stop in [0, 5, 17, 194]
                   for duration in [1, 4, 100]])
def test_start(start, stop, duration):
    animation = LinearFloatAnimation(start=start, stop=stop, duration=duration)
    assert animation[0] == start


@mark.parametrize("start, stop, duration",
                  [(start, stop, duration)
                   for start in [0, 1, 4, 17, 201]
                   for stop in [0, 5, 17, 194]
                   for duration in [1, 4, 100]])
def test_stop(start, stop, duration):
    animation = LinearFloatAnimation(start=start, stop=stop, duration=duration)
    assert animation[almost(duration)] == approx(stop)


@mark.parametrize("start, stop, duration",
                  [(start, stop, duration)
                   for start in [0, 1, 4, 17, 201]
                   for stop in [0, 5, 17, 194]
                   for duration in [1, 4, 100]])
def test_middle(start, stop, duration):
    animation = LinearFloatAnimation(start=start, stop=stop, duration=duration)
    expected = (start + stop) / 2
    assert animation[duration / 2] == approx(expected)
