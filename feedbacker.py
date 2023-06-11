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