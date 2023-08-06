from .models import SoundWave


def get_sound_data(sound: SoundWave):
    return [
        f"Sound information {sound.name}:",
        f"---------- {sound.name}: Sampling rate: {sound.sampling_rate} Hz",
        f"---------- {sound.name}: Path: {sound.path}"
    ]


def get_separator():
    return "********************************************************************"