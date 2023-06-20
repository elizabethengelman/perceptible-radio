from pydub import AudioSegment
from pydub.playback import play


class AudioGuider:
    def play_background_music(self):
        background = AudioSegment.from_mp3("./audio/background.mp3")
        play(background)

    def play_audio_1(self):
        audio_1 = AudioSegment.from_wav("./audio/1-intro.wav")
        play(audio_1 + 10)

    def play_audio_2(self):
        audio_2 = AudioSegment.from_wav("./audio/2-real-time.wav")
        play(audio_2 + 10)

    def play_audio_3(self):
        audio_3 = AudioSegment.from_wav("./audio/3-greenbank.wav")
        play(audio_3 + 10)

    def play_audio_4(self):
        audio_4 = AudioSegment.from_wav("./audio/4-outro.wav")
        play(audio_4 + 10)

# https://github.com/jiaaro/pydub
# background audio: https://creators.aiva.ai/