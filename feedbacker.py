import board
import neopixel

PIXEL_PIN = board.D21
NUM_PIXELS = 60


class Feedbacker:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS)

    def change(self, raw_data):
        real_r_g_b_tuple = map_raw_data_to_r_g_b(raw_data.real)
        imag_r_g_b_tuple = map_raw_data_to_r_g_b(raw_data.imag)
        for index, value in enumerate(self.pixels):
            if index % 2 != 0:
                self.pixels[index] = real_r_g_b_tuple
            else:
                self.pixels[index] = imag_r_g_b_tuple


def map_raw_data_to_r_g_b(raw_data_value):
    hex_value = map_raw_data_to_hex(raw_data_value)
    return hex_to_rgb(hex_value)


def map_num_to_range(num, inMin, inMax, outMin, outMax):
    return outMin + (float(num - inMin) / float(inMax - inMin) * (outMax - outMin))


def map_raw_data_to_hex(raw_data_value):
    # it is possible for these raw values to be negative, so the range is -1 to 1
    # mapping the raw data to a range that fits in the hex color range
    mapped_num = map_num_to_range(raw_data_value, -1, 1, 1000000, 16777215)
    rounded_mapped_number = round(mapped_num)
    # convert the mapped num decimal to a hex string, and then cut the x off the front
    return hex(rounded_mapped_number).split('x')[-1]


def hex_to_rgb(value):
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))
