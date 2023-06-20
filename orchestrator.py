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

stop_step_1 = False
stop_step_2 = False
stop_step_3 = False
stop_step_4 = False


# STEP 1
def start_intro_feedback():
    while True:
        print("pulse")
        time.sleep(1)
        if stop_step_1:
            break

# STEP 2


def start_radio_reader():
    print("starting radio reader")
    reader.start()


def start_realtime_feedbacker():
    while True:
        item = q.get()
        print("sending a new realtime value to the feedbacker")
        f.change(item)
        time.sleep(1)
        if stop_step_2:
            reader.stop()
            break


# STEP 3
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
            print("sending a new greenbank value to the feedbacker")
            f.change(complex_value)
            time.sleep(1)
            if stop_step_3:
                break

# STEP 4


def start_outro_feedback():
    while True:
        print("pulse")
        time.sleep(1)
        if stop_step_4:
            break


# Background music
play_background_music_thread = threading.Thread(target=audio.play_background_music)
print("starting background music")
play_background_music_thread.start()

time.sleep(5)

# Discrete sections
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SECTION 1~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 1: play the audio and have the feedbacker do real subtle pulsing
print("starting section 1")
play_audio_1_thread = threading.Thread(target=audio.play_audio_1)
play_audio_1_thread.start()

intro_feedback = threading.Thread(target=start_intro_feedback)
intro_feedback.start()

play_audio_1_thread.join()
stop_step_1 = True
# woah this fucking worked! i feel like if i just have a background audio that is on it's own thread group and never stops, maybe that'll work to make it not seem so disjointed?
print("phase 1 stopped")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SECTION 2~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# when that is finished, kick of step 2 (how do I do this piece?)
# 2: play audio 2, start the radio_reader and start_realtime_feedbacker
play_audio_2_thread = threading.Thread(target=audio.play_audio_2)
play_audio_2_thread.start()

radio_reader_thread = threading.Thread(target=start_radio_reader)
radio_reader_thread.start()

real_time_feedbacker_thread = threading.Thread(
    target=start_realtime_feedbacker)
real_time_feedbacker_thread.start()

play_audio_2_thread.join()
stop_step_2 = True
print("phase 2 stopped")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SECTION 3~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3:
play_audio_3_thread = threading.Thread(target=audio.play_audio_3)
play_audio_3_thread.start()

# this one will need to be handled differently depending on if im going to use real greenbank data, or fake it/cheat
# or maybe not, i probably have way more greenbank data than i need, so ill still probably want to stop it before i reach the end of the data
fake_greenbank_feedbacker_thread = threading.Thread(
    target=start_greenbank_feedbacker)
fake_greenbank_feedbacker_thread.start()

play_audio_3_thread.join()
stop_step_3 = True
print("phase 3 stopped")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SECTION 4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 4: Outro
play_audio_4_thread = threading.Thread(target=audio.play_audio_4)
play_audio_4_thread.start()

outro_feedback = threading.Thread(target=start_outro_feedback)
outro_feedback.start()

play_audio_4_thread.join()
stop_step_4 = True
print("goodbye!")


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
