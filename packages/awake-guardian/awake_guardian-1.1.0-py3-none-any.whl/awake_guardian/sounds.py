from .config import Audio, system

s = system()

if s == "Linux":
    from simpleaudio import WaveObject

    class Sound:
        @classmethod
        def remind(cls):
            cls.sound_remind = WaveObject.from_wave_file(Audio.coin)
            cls.sound_remind.play()

        @classmethod
        def nag(cls):
            cls.sound_nag = WaveObject.from_wave_file(Audio.wilhelm)
            cls.sound_nag.play()


elif s == "Windows":
    from playsound import playsound

    class Sound:
        @classmethod
        def remind(cls):
            playsound(Audio.coin)

        @classmethod
        def nag(cls):
            playsound(Audio.wilhelm)
