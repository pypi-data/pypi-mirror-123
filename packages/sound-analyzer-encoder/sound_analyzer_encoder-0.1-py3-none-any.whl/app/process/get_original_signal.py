import matplotlib.pyplot as plt
import numpy as np

from ..config import SOUND_RECORD_MIN
from .models import SoundWave
from .helpers import (
    get_sound_data,
    get_separator,
)

class GetOriginalSignal:

    data = []

    def handle(self, sound_waves: [SoundWave,]) -> [str,]:
        """
            use_case = GetOriginalSignal()
            data = use_case.handle(SignalWavesList().get_list())
            print(data)
            plt.show()
        """
        self.data.append(get_separator())
        self.data.append("Getting original signal of sounds loaded.")
        if len(sound_waves) < SOUND_RECORD_MIN:
            return [
                get_separator(),
                f"⚠️Load at least {SOUND_RECORD_MIN} sounds!"
            ]

        total_signal = np.ndarray([])

        length = len(sound_waves)
        fig, ax = plt.subplots(length+1, 1, sharex='col', figsize=(10, 16))
        plt.suptitle("Original signals")
        for i, sound in enumerate(sound_waves):
            self.data.extend(get_sound_data(sound))
            current_signal = sound.analog_signal[:-800, 0]
            ax[i].plot(current_signal)
            ax[i].set_title(sound.name)
            total_signal = total_signal + current_signal
        ax[length].plot(total_signal, color="g"); ax[length].set_title('All signals')           

        return self.data
