from textwrap import dedent

from pysim.actors.actor import Actor
from pysim.actors.channel import Channel
from pysim.actors.environment import export


class Environment:
    __channel: Channel[str]

    def __init__(self, channel: Channel[str]):
        self.__channel = channel

    @export
    def say(self, message: str):
        self.__channel.send(message)

    @export
    def hear(self) -> str:
        return self.__channel.receive()


def test_receiving():
    message = "test!"
    source = dedent(f'''
    say("{message}")
    ''')
    actor = Actor[str](source, Environment)
    assert actor.receive() == message


def test_echo():
    message = "repeated"
    source = dedent('''
    message = hear()
    say(message)    
    ''')
    actor = Actor[str](source, Environment)
    actor.send(message)
    assert actor.receive() == message
