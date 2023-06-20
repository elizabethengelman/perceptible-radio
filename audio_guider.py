from pydub import AudioSegment
from pydub.playback import play


class AudioGuider:
    def play_background_music(self):
        background = AudioSegment.from_mp3("./audio/background.mp3")
        play(background - 5)

    def play_audio_1(self):
        audio_1 = AudioSegment.from_wav("./audio/1-intro-short.wav")
        play(audio_1 + 5)

    def play_audio_2(self):
        audio_2 = AudioSegment.from_wav("./audio/2-real-time.wav")
        play(audio_2 + 5)

    def play_audio_3(self):
        audio_3 = AudioSegment.from_wav("./audio/3-greenbank.wav")
        play(audio_3 + 5)

    def play_audio_4(self):
        audio_4 = AudioSegment.from_wav("./audio/4-outro.wav")
        play(audio_4 + 5)

# https://github.com/jiaaro/pydub
# background audio: https://creators.aiva.ai/