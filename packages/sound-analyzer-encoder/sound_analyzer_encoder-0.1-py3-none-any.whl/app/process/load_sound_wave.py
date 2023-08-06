from datetime import datetime

import scipy.io.wavfile as wavfile
import pyaudio
import wave

from ..config import (
    RESOURCES_PATH,
    BASE_DIR,
    DATETIME_FORMAT,
    RECORD_SECONDS
)
from .helpers import (
    get_sound_data,
    get_separator,
)
from .models import SoundWave


class LoadSoundWave:

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 16000
    data = []

    def handle(self) -> (SoundWave, [str,]):
        """
            use_case = LoadSoundWave()
            sound_wave, data = use_case.handle()
            SoundWaveList().append_sound(sound_wave)
            print(data)
        """
        self.data.extend([
            get_separator(),
            "Loading sound waves.",
            f"Channels: {self.CHANNELS}",
            f"Chunk: {self.CHUNK}",
            f"Format: {self.FORMAT}",
        ])
        today = datetime.today()
        file_name = f"output{str(today.strftime(DATETIME_FORMAT))}.wav"
        output_filepath = RESOURCES_PATH + "/" + file_name

        self.record(output_filepath)

        s_rate, analog_signal = wavfile.read(BASE_DIR + output_filepath[3:])

        s = SoundWave()
        s.name = file_name
        s.sampling_rate = s_rate
        s.path = output_filepath
        s.analog_signal = analog_signal
        self.data.extend(get_sound_data(s))

        return s, self.data

    def record(self, output_filepath: str = ""):
        p = pyaudio.PyAudio()

        stream = p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        print("* Recording *")

        frames = []

        for _ in range(0, int(self.RATE / self.CHUNK * RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        print("* Done recording *")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(output_filepath, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
