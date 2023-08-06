from numpy import array

class Singleton(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class SoundWave:

    analog_signal: array = None
    sampling_rate: int = 0
    name: str = ""
    path: str = ""

class SoundWaveList(Singleton):

    sound_waves: list = []

    def append_sound(self, s: SoundWave):
        self.sound_waves.append(s)

    def get_list(self):
        return self.sound_waves
