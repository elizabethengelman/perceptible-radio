"""
This is the orchestrator process.

To start it will be responsible for starting the radio-reader and the feedbacker in two different threads with a shared queue
"""

from queue import Queue
import threading
import time
from radio_reader import RadioReader
from feedbacker import Feedbacker

q = Queue()
reader = RadioReader(q)
f = Feedbacker()


def radio_reader():
    reader.start()


def feedbacker():
    while True:
        item = q.get()
        f.change(item)
        time.sleep(2)


radio_reader_thread = threading.Thread(target=radio_reader)
radio_reader_thread.start()

feedbacker_thread = threading.Thread(target=feedbacker)
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
