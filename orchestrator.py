"""
This is the orchestrator process.

To start it will be responsible for starting the radio-reader and the feedbacker in two different threads with a shared queue
"""

from queue import Queue
import threading
import time
from radio_reader import RadioReader
from feedbacker import Feedbacker
from audio_guider import AudioGuider
import numpy

q = Queue()
reader = RadioReader(q)
f = Feedbacker()
audio = AudioGuider()


def start_radio_reader():
    reader.start()

# def stop_radio_reader():
  # can i do this by having the sdr instace be on the radioreader class, and then call cancel_async whatever method


def start_realtime_feedbacker():
    while True:
        item = q.get()
        f.change(item)
        time.sleep(1)


def get_greenbank_data():
    april_23_file = open("./2023-04-23", "r")
    april_23_data = april_23_file.read()
    april_23_file.close()
    parsed_into_lines = april_23_data.split("\n")

    # each "sample" is 1024 individual readings, i think
    # i think that this method should return a similar shape to the real-time data
    # and the real-time data will be further split to send each individual sample to the queue one at a time
    samples_to_return = []
    for line in parsed_into_lines:
        sample = line.split(", ")
        # the first element looks like this: '[(0.12941176470588234-0.027450980392156876j)'
        # and this is removing the left square bracket
        sample[0] = sample[0][1:]
        # the last element looks like this: '(-0.11372549019607847+0.08235294117647052j)]'
        # and this is removing the right square bracket
        sample[-1] = sample[-1][:-1]
        samples_to_return.append(sample)
        return samples_to_return


def start_greenbank_feedbacker():
    greenbank_data = get_greenbank_data()
    for sample in greenbank_data:
        for individual_reading in sample:
            complex_value = numpy.complex128(individual_reading)
            # sample = [complex_value.real, complex_value.imag]
            f.change(complex_value)
            time.sleep(2)


play_audio_1_thread = threading.Thread(target=audio.play_audio_1)
play_audio_1_thread.start()

# radio_reader_thread = threading.Thread(target=start_radio_reader)
# radio_reader_thread.start()

# feedbacker_thread = threading.Thread(target=start_realtime_feedbacker)
# feedbacker_thread.start()



"""
Brainstorming:
- it would be cool if there was a subtle fade in and out at the beginning
- also, it may be too much but wouldn't it be cool if i could also play real live radio
"""


# TODO: graceful exit & cleanup

"""
* i had been blocking on the feedbacker_thread, but then when i removed that, it didn't seem to change the outcome that much
  i should keep an eye on this - i wonder if its that we will block putting stuff onto the queue while we're doing the feedbacker stuff
  feedbacker_thread.join()

* https://www.geeksforgeeks.org/queue-in-python/
* https://pymotw.com/2/Queue/
* https://www.tutorialspoint.com/how-to-implement-multithreaded-queue-with-python
* https://docs.python.org/3/library/queue.html#module-queue
* https://www.troyfawkes.com/learn-python-multithreading-queues-basics/
* https://chat.openai.com/
"""
