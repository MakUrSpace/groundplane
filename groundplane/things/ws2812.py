""" Control a strip of ws2812 LEDs """
from rpi_ws281x import PixelStrip, Color

from groundplane.things import thing


colors = {
    "white": Color(255, 255, 255),
    "blue": Color(0, 0, 255),
    "green":  Color(0, 255, 0),
    "red": Color(255, 0, 0),
    "off": Color(0, 0, 0)
}


def identify_color(color):
    if color in colors:
        return color
    for tcn, test_color in colors.items():
        if test_color == color:
            return tcn
    raise Exception(f"Color ({color}) not recognized")


class ws2812(thing):
    def __init__(self, SORT, DEVICE_TYPE, PIN=18, LEDS=32, DCOLOR='white'):
        super().__init__(SORT, DEVICE_TYPE="WS2812")
        assert PIN in [18, 13]
        assert DCOLOR.lower() in colors

        self.DCOLOR = DCOLOR
        self.PIN = PIN

        self.strip = PixelStrip(num=LEDS, pin=PIN, freq_hz=800000, dma=10, invert=False, brightness=255, channel=0)
        self.strip.begin()
        self.color = colors[DCOLOR]

    def state(self):
        state = super().state()
        state['state'] = identify_color(self.color)

    def set_strip_to_color(self, color=None):
        color = self.DCOLOR if color is None else color
        assert type(color) == str
        color = colors[color.lower()]
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def request_state(self, requested_state):
        next_color = requested_state.get("state", self.DCOLOR)
        next_color =  colors.get(next_color, identify_color(next_color))
        next_color = identify_color(next_color)
        self.color = next_color
        self.set_strip_to_color(self.color)
        return True

