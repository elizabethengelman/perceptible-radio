"""
This is the orchestrator process.

To start it will be responsible for starting the radio-reader and the feedbacker in two different threads with a shared queue
"""

from queue import Queue
import threading
import time
from radio_reader import RadioReader
from feedbacker import Feedbacker
import numpy

q = Queue()
reader = RadioReader(q)
f = Feedbacker()


def start_radio_reader():
    reader.start()

# def stop_radio_reader():
  # can i do this by having the sdr instace be on the radioreader class, and then call cancel_async whatever method


def start_realtime_feedbacker():
    while True:
        item = q.get()
        f.change(item)
        time.sleep(2)


def get_greenbank_data():
    april_23_file = open("./2023-04-23", "r")
    april_23_data = april_23_file.read()
    april_23_file.close()

    parsed_data = april_23_data.split(", ")

    # the first element looks like this: '[(0.12941176470588234-0.027450980392156876j)'
    # and this is removing the left square bracket
    parsed_data[0] = parsed_data[0][1:]

    # the last element looks like this: '(-0.11372549019607847+0.08235294117647052j)]'
    # and this is removing the right square bracket
    parsed_data[-1] = parsed_data[-1][:-1]

    return parsed_data

def start_greenbank_feedbacker():
    greenbank_data= get_greenbank_data()
    for data_string in greenbank_data:
        complex_value = numpy.complex128(data_string)
        sample = [complex_value.real, complex_value.imag]
        f.change(sample)
        time.sleep(2)


radio_reader_thread = threading.Thread(target=start_radio_reader)
radio_reader_thread.start()

feedbacker_thread = threading.Thread(target=start_realtime_feedbacker)
feedbacker_thread.start()

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
