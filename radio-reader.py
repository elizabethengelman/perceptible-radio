# This is based on the prototype for my Make Art with AI that used rtlsdr samples to manipulate the playback of some AI generated audio
# https://pypi.org/project/pyrtlsdr/
from rtlsdr import RtlSdr

def callback(samples, context):
    convertedSamples = []
    for sample in samples:
      convertedSamples.append([sample.real, sample.imag]) 

    print("samples: ", convertedSamples) # put these on the queue instead


sdr = RtlSdr()
# configure device
sdr.sample_rate = 2.048e6  # 2048000 Hz
sdr.center_freq = 8.91e7  # 89100000 Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'
sdr.read_samples_async(callback, num_samples=512) # this defaults to reading 1024 samples

"""
Notes/thoughts/questions:
* each sample is a numpy.complex128, which has a real and an imaginary part, with methods for each
* I'm wondering if i should have the lights change for each sample set? or for each individual sample maybe ill just make that decision later
"""