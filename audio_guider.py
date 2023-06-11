from playsound import playsound
import threading
import time


def play_audio_1():
    playsound("radio-waves-sound-walk-3.mp3")


def play_audio_2():
    time.sleep(0.5)
    playsound("radio-waves-sound-walk-3.mp3")


play_audio_1_thread = threading.Thread(target=play_audio_1)
play_audio_1_thread.start()

play_audio_2_thread = threading.Thread(target=play_audio_2)
play_audio_2_thread.start()
