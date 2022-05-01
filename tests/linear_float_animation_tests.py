from math import ulp

from pytest import approx
from pytest import mark

from pysim.graphics.animations.float import LinearFloatAnimation


def almost(n):
    return n - ulp(n)


@mark.parametrize("start, stop, duration",
                  [(start, stop, duration)
                   for start in range(1, 10)
                   for stop in range(1, 10)
                   for duration in
                   range(1, 10)])
def test_start(start, stop, duration):
    animation = LinearFloatAnimation(start=start, stop=stop, duration=duration)
    assert animation[0] == start


@mark.parametrize("start, stop, duration",
                  [(start, stop, duration)
                   for start in range(1, 10)
                   for stop in range(1, 10)
                   for duration in range(1, 10)])
def test_stop(start, stop, duration):
    animation = LinearFloatAnimation(start=start, stop=stop, duration=duration)
    assert animation[almost(duration)] == approx(stop)


@mark.parametrize("start, stop, duration",
                  [(start, stop, duration)
                   for start in range(1, 10)
                   for stop in range(1, 10)
                   for duration in range(1, 10)])
def test_middle(start, stop, duration):
    animation = LinearFloatAnimation(start=start, stop=stop, duration=duration)
    expected = (start + stop) / 2
    assert animation[duration / 2] == approx(expected)
