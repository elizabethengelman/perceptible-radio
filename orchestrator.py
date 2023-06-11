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
  #can i do this by having the sdr instace be on the radioreader class, and then call cancel_ascyn whatever method 


def start_realtime_feedbacker():
    while True:
        item = q.get()
        f.change(item)
        time.sleep(2)


def start_greenbank_feedbacker():
    greenbank_data = [(0.26274509803921564+0.28627450980392166j), (-0.2313725490196078-0.16078431372549018j),
                      (-0.0117647058823529+0.10588235294117654j), (-0.14509803921568631-0.19999999999999996j)]
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
