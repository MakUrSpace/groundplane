""" Control a strip of ws2812 LEDs """
from rpi_ws281x import PixelStrip, Color

from groundplane.things import thing


colors = {
    "white": Color(255, 255, 255)
    "blue": Color(0, 0, 255)
    "green":  Color(0, 255, 0)
    "red": Color(255, 0, 0)
    "off": Color(0, 0, 0)
}


def identify_color(color):
    for tcn, test_color in colors.items():
	if test_color == color:
	    return tcn
    raise Exception(f"Color ({color}) not recognized")


class ws2812(thing):
    def __init__(self, SORT, PIN="GPIO18", LEDS=32, DCOLOR='white'):
        super().__init__(SORT, DEVICE_TYPE="WS2812", PIN=PIN, LEDS=LEDS, DCOLOR=DCOLOR)
        assert PIN in ['GPIO18', 'GPIO13']
	assert identify_color(DCOLOR)
        LED_FREQ_HZ = 800000
        LED_DMA = 10
        LED_BRIGHTNESS = 255
        LED_INVERT = False
        LED_CHANNEL = 0
        self.strip = PixelStrip(LEDS, PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_CHANNEL)
        self.strip.begin()
        self.dcolor = DCOLOR
	self.color = colors[DCOLOR]

    def state(self):
	state = super().state()
	state['state'] = identify_color(self.color)

    def set_strip_to_color(self, color):
	for i in range(strip.NumPixels()):
	   strip.setPixelColor(i, color)

    def request_state(requested_state):
        next_color = requested_state.get("state", self.dcolor)
        next_color = identify_color(next_color)
        self.color = next_color
        self.set_strip_to_color(self.color)
        return True

