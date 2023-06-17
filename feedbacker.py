import board
import neopixel

PIXEL_PIN = board.D21
NUM_PIXELS = 60

class Feedbacker:
  def __init__(self):
    self.pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS)
    self.rValue = 255 
    self.gValue = 0
    self.bValue = 0

  def change(self, raw_data):
    self.pixels.fill((self.rValue, self.gValue, self.bValue))
    self.incrementTheRGBValue()

  def incrementTheRGBValue(self):
    if self.rValue == 255:
      self.rValue = 0
    else:
      self.rValue = self.rValue + 1

    if self.gValue == 255:
      self.gValue = 0
    else:
      self.gValue = self.gValue + 1

    if self.bValue == 255:
      self.bValue = 0
    else:
      self.bValue = self.bValue + 1

def map_raw_data_to_hex(raw_data_value):
  # it is possible for these raw values to be negative, so the range is -1 to 1
  mapped_num = map_num_to_range(raw_data_value, -1, 1, 0, 16777215) # mapping the raw data to a range that fits in the hex color range
  return round(mapped_num)


def map_num_to_range(num, inMin, inMax, outMin, outMax):
  return outMin + (float(num - inMin) / float(inMax - inMin) * (outMax - outMin))