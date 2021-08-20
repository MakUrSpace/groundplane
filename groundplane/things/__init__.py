from groundplane.things.thing import thing
from groundplane.things.gpio import latch, mag_sensor
from groundplane.things.camera import camera
from groundplane.things.wemo import wemo_plug, wemo_insight
from groundplane.things.kasa import kasa_strip
from groundplane.things.ws2812 import ws2812


def get_subclasses(root):
    return [root, *[leaf for sub in root.__subclasses__() for leaf in get_subclasses(sub)]]


thing_types = {subthing.__name__: subthing for subthing in get_subclasses(thing)}
