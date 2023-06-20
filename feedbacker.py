import board
import neopixel
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.sequence import AnimationSequence

PIXEL_PIN = board.D21
NUM_PIXELS = 60


class Feedbacker:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, auto_write=False, brightness=0.1)
        self.power_readings = []
        self.intro = Pulse(self.pixels, speed=0.3, color=(0, 0, 255))
        self.realtime = Chase(self.pixels, speed=0.1, color=(0, 255, 0), size=3, spacing=6)
        self.greenbank = Chase(self.pixels, speed=0.3, color=(255, 0, 0), size=3, spacing=6)
        self.outro = Pulse(self.pixels, speed=0.3, color=(0, 0, 255))
        self.animations = AnimationSequence(self.intro, self.realtime, self.greenbank, self.outro)

    def change(self, raw_data):
        signal_power = get_signal_power(raw_data)
        self.power_readings.append(signal_power)

        avg = sum(self.power_readings) / len(self.power_readings)
        print("AVERAGE POWER READING: ", avg)

        mapped_to_color_range = map_power_value_to_hex(signal_power)

        rgb_tuple = hex_to_rgb(mapped_to_color_range)
        inverse_rgb_tuple = get_inverse_color(rgb_tuple)
        print("rgb: ", rgb_tuple)
        print("inverse rgb: ", inverse_rgb_tuple)

        # https://www.techiedelight.com/loop-through-list-with-index-python/
        for index, value in enumerate(self.pixels):
            if index % 2 != 0:
                self.pixels[index] = rgb_tuple
            else:
                self.pixels[index] = inverse_rgb_tuple


# TODO: move this into radio_reader?
def get_signal_power(raw_data):
    real_squared = raw_data.real ** 2
    imag_squared = raw_data.imag ** 2
    return real_squared + imag_squared


# https://www.30secondsofcode.org/python/s/num-to-range/
def map_num_to_range(num, inMin, inMax, outMin, outMax):
    return outMin + (float(num - inMin) / float(inMax - inMin) * (outMax - outMin))


def map_power_value_to_hex(power_value):
    # now that we're using power, i dont think that'll ever be less than zero
    print("power: ", power_value)
    mapped_num = map_num_to_range(power_value, 0, 1, 1000000, 16777215)
    rounded_mapped_number = round(mapped_num)
    # convert the mapped num decimal to a hex string, and then cut the x off the front
    return hex(rounded_mapped_number).split('x')[-1]


#https://www.educative.io/answers/how-to-convert-hex-to-rgb-and-rgb-to-hex-in-python
def hex_to_rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)

    return tuple(rgb)


def get_inverse_color(rgb_value):
    original_r = rgb_value[0]
    original_g = rgb_value[1]
    original_b = rgb_value[2]
    new_r = (original_r * -1) + 255
    new_g = (original_g * -1) + 255
    new_b = (original_b * -1) + 255
    return (new_r, new_g, new_b)


# neopixel library: https://docs.circuitpython.org/projects/neopixel/en/latest/api.html
# https://learn.adafruit.com/adafruit-neopixel-uberguide/python-circuitpython