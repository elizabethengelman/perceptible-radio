import board
import neopixel

PIXEL_PIN = board.D21
NUM_PIXELS = 60

class Feedbacker:
  def __init__(self):
    self.pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS)

  def start(self):
    print("starting the light changes")

# >>> import board
# >>> import neopixel
# >>> pixels = neopixel.NeoPixel(board.D21, 60)
# >>> pixels[0] = (255, 0, 0)