
import matplotlib.pyplot as plt
import numpy as np
import math

from ..config import SOUND_RECORD_MIN
from .models import SoundWave
from .helpers import get_separator


class EncodeSignal:

    BITS = 5
    VOLTAGE = 20
    L = 50 # number of digital samples per data bit
    data = []

    def __init__(self):
        self.RESOLUTION = self.VOLTAGE/(math.pow(2, self.BITS))

    def handle(self, sound_waves: [SoundWave,], limit = 1000000) -> [str,]:
        """
            use_case = EncodeSignal()
            data = use_case.handle(
                SignalWavesList().get_list(),
                1000000
            )
            print(data)
            plt.show()
        """
        self.data.extend([
            get_separator(),
            "Encoding signal with Differential Manchester encoding (DM).",
            f"Bits {self.BITS}",
            f"Voltage {self.VOLTAGE}",
            f"Digital samples per data bit: {self.L}",
            f"Resolution: {self.RESOLUTION}",
        ])
        if len(sound_waves) < SOUND_RECORD_MIN:
            return [
                get_separator(),
                f"⚠️Load at least {SOUND_RECORD_MIN} sounds!"
            ]

        self.data.append(f"Limit of data: {limit}. (Show only last {limit} data)")
        signal = np.ndarray([])
        for sound in sound_waves:
            signal = signal + sound.analog_signal[:-800, 0]
        digital_signal = self.analog_to_digital(signal)

        end = -limit
        encoded_signal = self.encode_signal(digital_signal)

        fig, ax = plt.subplots(3, 1, sharex='col', figsize=(10, 16))
        plt.suptitle("Differential Manchester encoding. Please zoom in to see details.")
        ax[0].plot(self.get_clock(len(digital_signal))[end:]); ax[0].set_title('CLK')
        ax[1].plot(self.get_seq(digital_signal, 2)[end:]); ax[1].set_title('Digital Data')
        ax[2].plot(self.get_seq(encoded_signal)[end:]); ax[2].set_title('Differential Manchester')
        
        return self.data

    def analog_to_digital(self, analog_signal):
        return [np.around(a/self.RESOLUTION) if a>0 else 0 for a in analog_signal]

    def get_clock(self, length):
        _ = np.arange(0, 2*length) % 2
        return self.get_seq(_)

    def get_seq(self, array, multiplier = 1):
        return np.repeat(array, self.L*multiplier)

    def encode_signal(self, digital_signal: list) -> list:
        manchester = list(digital_signal) # Duplicate signal
        previous_voltage = self.VOLTAGE

        result = []
        # TODO: Improve for
        for ii in range(0, len(manchester)):
            if (manchester[ii] > 0) and (previous_voltage < 0):
                result.extend((-self.VOLTAGE, self.VOLTAGE))
                previous_voltage = self.VOLTAGE
            elif (manchester[ii] > 0) and (previous_voltage > 0):
                result.extend((self.VOLTAGE, -self.VOLTAGE))
                previous_voltage = -self.VOLTAGE
            elif (manchester[ii] == 0) and (previous_voltage > 0):
                result.extend((-self.VOLTAGE, self.VOLTAGE))
                previous_voltage = self.VOLTAGE
            elif (manchester[ii] == 0) and (previous_voltage < 0):
                result.extend((self.VOLTAGE, -self.VOLTAGE))
                previous_voltage = -self.VOLTAGE
        return result