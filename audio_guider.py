from playsound import playsound
import threading
import time

class AudioGuider:
    def play_audio_1(self):
        playsound("./audio/1-intro.m4a")


    def play_audio_2(self):
        playsound("./audio/2-real-time-data.m4a")


    def play_audio_3(self):
        playsound("./audio/3-greenbank-data.m4a")


    def play_audio_4(self):
        playsound("./audio/4-outro.m4a")


# play_audio_1_thread = threading.Thread(target=play_audio_1)
# play_audio_1_thread.start()

# play_audio_2_thread = threading.Thread(target=play_audio_2)
# play_audio_2_thread.start()
