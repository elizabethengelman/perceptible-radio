# This is based on the prototype for my Make Art with AI that used rtlsdr samples to manipulate the playback of some AI generated audio
# https://pypi.org/project/pyrtlsdr/
from rtlsdr import RtlSdr
sdr = RtlSdr()
# configure device
sdr.sample_rate = 2.048e6  # 2048000 Hz
sdr.center_freq = 8.91e7  # 89100000 Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'
samples = sdr.read_samples(512)

arrayOfSamples = []

# each sample is a numpy.complex128, which has a real and an imaginary part, with methods for each
# so to make this into something that I can use in javascript a bit more easier...
for sample in samples:
    arrayOfSamples.append([sample.real, sample.imag])

json = {"data": arrayOfSamples}

print(json)


"""
from this resource: https://arachnoid.com/software_defined_radios/
"vectors are just numbers with two (or more) components" so i think that these I/Q data are vectors - it would be cool
if i could use this and create a visualization like some of the vector tuts for p5js
"The terms I and Q actually have a meaning — I means "Inphase" and Q means "Quadrature" (more detail). I mention this because the use of I for the real component, and Q
 for the imaginary component, of a complex number seems perversely confusing"
"""

"""
# https://www.reddit.com/r/RTLSDR/comments/1xo5l3/help_me_make_sense_of_rtl2832u_raw_iq_data/
* one answer here said that sdrs output quadrature waveform data - which means that each sample contains both magnitude
  and phase info 
* so in the case of RTL a sample contains an 8-bit (real) component and an 8-bit Q (imaginary) component, which represent
  one point in time

okay, this is definitely what my samples from Greenbank are, so that's exciting!!
but like wtf do i do with that?
"""
