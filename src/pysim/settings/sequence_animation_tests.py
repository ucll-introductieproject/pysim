from math import ulp

from pytest import approx
from pytest import mark

from pysim.graphics.animations.float import LinearFloatAnimation
from pysim.graphics.animations.sequence import SequenceAnimation


def almost(n):
    return n - ulp(n)


@mark.parametrize("child_durations", [
    [],
    [1],
    [1, 1],
    [1, 1, 1],
    [1, 2],
    [1, 2, 3]
])
def test_duration(child_durations):
    children = [LinearFloatAnimation(0, 1, duration) for duration in child_durations]
    expected = sum(child_durations)
    animation = SequenceAnimation(children)
    assert animation.duration == approx(expected)


@mark.parametrize('children, pairs', [
    (
            [LinearFloatAnimation(0, 1, 1)],
            [(0, 0), (0.5, 0.5), (almost(1), 1)]
    ),
    (
            [LinearFloatAnimation(0, 1, 1), LinearFloatAnimation(1, 0, 1)],
            [(0, 0), (0.5, 0.5), (1, 1), (1.5, 0.5), (almost(2), 0)]
    ),
    (
            [LinearFloatAnimation(0, 1, 1), LinearFloatAnimation(1, 0, 2)],
            [(0, 0), (0.5, 0.5), (1, 1), (2, 0.5), (almost(3), 0)]
    ),
    (
            [LinearFloatAnimation(0, 1, 1), LinearFloatAnimation(1, 0, 1), LinearFloatAnimation(0, 1, 1)],
            [(0, 0), (0.5, 0.5), (1, 1), (1.5, 0.5), (2, 0), (2.5, 0.5), (almost(3), 1)]
    ),
])
def test_values(children, pairs):
    animation = SequenceAnimation(children)
    for time, expected_value in pairs:
        assert animation[time] == approx(expected_value)
