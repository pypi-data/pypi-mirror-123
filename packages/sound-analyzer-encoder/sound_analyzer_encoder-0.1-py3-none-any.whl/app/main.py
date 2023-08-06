import sys
import os
from os.path import isfile, join
from time import sleep

from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from .interface import *
from .config import (
    RESOURCES_PATH,
    RECORD_SECONDS
)
from .process.models import SoundWaveList
from .process.load_sound_wave import LoadSoundWave
from .process.perform_fourier_analysis import PerformFourierAnalysis
from .process.get_original_signal import GetOriginalSignal
from .process.encode_signal import EncodeSignal as EncodeSignalUseCase


def print_loading_graph_plot(ui, list_files):
    list_files = list(dict.fromkeys(list_files))
    for i, v in enumerate(list_files):
        ui.verticalLayout_5.addWidget(QtWidgets.QLabel(v))
    ui.scrollAreaWidgetContents_2.setLayout(ui.verticalLayout_5)


def delete_resource_files():
    all_files = os.listdir(f"{RESOURCES_PATH}/")
    for item in all_files:
        if item.endswith(".wav"): os.remove(RESOURCES_PATH + "/" + item)


class MiApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.perfom_fa.clicked.connect(self.perform_fa_graphic)
        self.ui.show_original_buttom.clicked.connect(self.original_signal_graphic)
        self.ui.encode_buttom.clicked.connect(self.encode_signal_graphic)
        self.ui.pushButton.clicked.connect(self.print_files)

    def perform_fa_graphic(self):
        PerformFA(self.ui)

    def original_signal_graphic(self):
        OriginalSound(self.ui)

    def encode_signal_graphic(self):
        EncodeSignal(self.ui)

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def print_files(self):
        self.ui.listWidget.clear()
        loading = Load(self.ui)
        loading.create_file()
        list_files = loading.return_files()
        for inx, val in enumerate(list_files):
            if inx > 0: self.ui.listWidget.insertItem(inx, val)

class PerformFA:

    def __init__(self, ui):

        use_case = PerformFourierAnalysis()
        data = use_case.handle(SoundWaveList().get_list())
        print_loading_graph_plot(ui, data)
        plt.show()


class OriginalSound:

    def __init__(self, ui):
        use_case = GetOriginalSignal()
        data = use_case.handle(SoundWaveList().get_list())
        print_loading_graph_plot(ui, data)
        plt.show()

class EncodeSignal:

    def __init__(self, ui):
        use_case = EncodeSignalUseCase()
        data = use_case.handle(
            SoundWaveList().get_list(),
            1000000
        )
        print_loading_graph_plot(ui, data)
        plt.show()


class Load:

    def __init__(self, ui):
        self.ui = ui

    def create_file(self):
        use_case = LoadSoundWave()
        sound_wave, data = use_case.handle()
        SoundWaveList().append_sound(sound_wave)
        print_loading_graph_plot(self.ui, data)

    def return_files(self):
        return [f for f in os.listdir(RESOURCES_PATH) if isfile(join(RESOURCES_PATH, f))]
