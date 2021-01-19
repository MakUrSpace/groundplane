from .thing import thing
from .gpio import latch, mag_sensor
from .camera import camera
from .wemo import wemo_plug, wemo_insight


def get_subclasses(root):
    return [root, *[leaf for sub in root.__subclasses__() for leaf in get_subclasses(sub)]]


thing_types = {subthing.__name__: subthing for subthing in get_subclasses(thing)}
