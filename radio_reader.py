# This is based on the prototype for my Make Art with AI that used rtlsdr samples to manipulate the playback of some AI generated audio
# https://pypi.org/project/pyrtlsdr/
from rtlsdr import RtlSdr


class RadioReader:
    def __init__(self, shared_queue):
        self.shared_queue = shared_queue
        self.sdr = RtlSdr()

    def start(self):
        # configure device
        self.sdr.sample_rate = 2.048e6  # 2048000 Hz
        self.sdr.center_freq = 8.95e7  # 89100000 Hz
        self.sdr.freq_correction = 60   # PPM
        self.sdr.gain = 'auto'
        # this defaults to reading 1024 samples
        self.sdr.read_samples_async(self.callback, num_samples=512)

    def stop(self):
        self.sdr.cancel_read_async()

    def callback(self, samples, context):
        for sample in samples:
            self.shared_queue.put(sample)


"""
Notes/thoughts/questions:
* each sample is a numpy.complex128, which has a real and an imaginary part, with methods for each
* I'm wondering if i should have the lights change for each sample set? or for each individual sample maybe ill just make that decision later
"""
