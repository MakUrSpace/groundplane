from groundplane.things.thing import thing

try:
    from groundplane.things.gpio import latch, mag_sensor
except ImportError:
    print("WARNING: Unable to import gpio definition")

try:
    from groundplane.things.wemo import wemo_plug, wemo_insight
except ImportError:
    print("WARNING: Unable to import wemo definitions")

try:
    from groundplane.things.kasa import kasa_strip
except ImportError:
    print("WARNING: Unable to import kasa definition")

try:
    from groundplane.things.ws2812 import ws2812
except ImportError:
    print("WARNING: Unable to import ws2812 definition")

try:
    from groundplane.things.max31855 import max31855
except ImportError:
    print("WARNING: Unable to import max31855 definition")


def thing_types(refresh=False):
    if refresh or thing_types.thing_types is None:
        def get_subclasses(root):
            return [root, *[leaf for sub in root.__subclasses__() for leaf in get_subclasses(sub)]]
        
        thing_types.thing_types = {subthing.__name__: subthing for subthing in get_subclasses(thing)}
    return thing_types.thing_types


thing_types.thing_types = None
