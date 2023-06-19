# based on https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
import time
import board
import neopixel


# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D21

num_pixels = 60

pixels = neopixel.NeoPixel(pixel_pin, num_pixels,
                           brightness=0.2, auto_write=False)


steps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]


def pulse():
    pixels.fill((0, 0, 255))
    for step in steps:
        pixels.brightness = step
        pixels.show()


pulse()
# def wheel(pos):
#     # Input a value 0 to 255 to get a color value.
#     # The colours are a transition r - g - b - back to r.
#     if pos < 0 or pos > 255:
#         r = g = b = 0
#     elif pos < 85:
#         r = int(pos * 3)
#         g = int(255 - pos * 3)
#         b = 0
#     elif pos < 170:
#         pos -= 85
#         r = int(255 - pos * 3)
#         g = 0
#         b = int(pos * 3)
#     else:
#         pos -= 170
#         r = 0
#         g = int(pos * 3)
#         b = int(255 - pos * 3)
#     print((r, g, b))
#     return (r, g, b)


# def rainbow_cycle(wait):
#     for j in range(255):
#         for i in range(num_pixels):
#             pixel_index = (i * 256 // num_pixels) + j
#             pixels[i] = wheel(pixel_index & 255)
#         pixels.show()
#         time.sleep(wait)


# while True:
#     pixels.fill((255, 0, 0))
#     pixels.show()
#     time.sleep(1)

#     pixels.fill((0, 255, 0))
#     pixels.show()
#     time.sleep(1)

#     pixels.fill((0, 0, 255))
#     pixels.show()
#     time.sleep(1)

#     rainbow_cycle(0.001)
