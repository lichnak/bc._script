import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QPushButton,\
QLabel, QRadioButton, QSlider,  QButtonGroup, QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import csv
from scipy import signal
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

# from mainWin import data
# from mainWin import my_channel
# import random

class Filtrace(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'XRD data filtering'
        self.width = 720
        self.height = 550

        self.m = PlotCanvas(self, width=7.05, height=4)
        self.m.move(7, 7)
        self.tools = NavigationToolbar(self.m, self)
        self.tools.move(7, 513)
        self.tools.resize(417, 30)

        self.label0 = QLabel('Select data filter and its parameters', self)
        self.labelx = QLabel('Export file', self)
        self.rad1 = QRadioButton("&Zero-phase")
        self.rad2 = QRadioButton("&Savitzky-Golay")
        self.rad3 = QRadioButton("&Median")
        self.rad4 = QRadioButton("&Exponential smoothing")
        self.slide1 = QSlider(Qt.Horizontal)
        self.slide2 = QSlider(Qt.Horizontal)

        self.data = np.genfromtxt('testovaci.dat')

        self.my_channel = 6

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMaximumSize(720, 550)

        self.layout1 = QHBoxLayout()
        self.layout2 = QHBoxLayout()

        widget1 = QWidget(self)
        widget2 = QWidget(self)
        widget1.setLayout(self.layout1)
        widget2.setLayout(self.layout2)
        widget1.resize(420, 35)
        widget1.move(10, 440)
        widget2.resize(420, 35)
        widget2.move(10, 468)

        self.layout1.addWidget(self.rad1)
        self.layout2.addWidget(self.rad2)
        self.layout1.addWidget(self.rad3)
        self.layout2.addWidget(self.rad4)
        self.layout1.addWidget(self.slide1)
        self.layout2.addWidget(self.slide2)

        group = QButtonGroup(self)
        group.addButton(self.rad1)
        group.addButton(self.rad2)
        group.addButton(self.rad3)
        group.addButton(self.rad4)

        self.label0.move(15, 412)
        self.label0.resize(250, 26)
        self.label0.setFont(QFont("Sans Serif", 11))

        self.labelx.move(545, 412)
        self.labelx.resize(150, 26)
        self.labelx.setFont(QFont("Sans Serif", 11))

        self.rad1.setChecked(False)
        self.rad1.toggled.connect(lambda: self.m.rad1click(self.data, self.my_channel))
        self.rad2.setChecked(False)
        self.rad2.toggled.connect(lambda: self.m.rad2click(self.data, self.my_channel))
        self.rad3.setChecked(False)
        self.rad4.setChecked(False)

        self.slide1.move(300, 441)
        self.slide1.setMaximumWidth(110)
        self.slide1.setMinimum(11)
        self.slide1.setMaximum(1001)
        self.slide1.setToolTip('Window length')
        self.slide1.setSingleStep(1)
        self.slide1.setTickInterval(100)
        self.slide1.setTickPosition(QSlider.TicksBelow)
        self.slide1.setFocusPolicy(Qt.StrongFocus)

        self.slide2.move(300, 472)
        self.slide2.setMaximumWidth(110)
        self.slide2.setMinimum(1)
        self.slide2.setMaximum(100)
        self.slide2.setToolTip('Alpha parameter')
        self.slide2.setSingleStep(1)
        self.slide2.setTickInterval(10)
        self.slide2.setTickPosition(QSlider.TicksBelow)
        self.slide2.setFocusPolicy(Qt.StrongFocus)

        self.m.plot(self.data, self.my_channel)

        self.show()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=7.05, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)


        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


    def plot(self, data_plt, channel):
        self.my_channel = channel
        self.data = data_plt
        ax = self.figure.add_subplot(111)
        ax.autoscale(enable=True, axis='x', tight=bool)

        row = data_plt.shape[0]
        col = data_plt.shape[1]
        data_plt = data_plt[:, 7:col]

        r = data_plt[:, 149]
        s = np.arange(0, row, 1)

        ax.plot(s, r, linewidth=0.5, c=[0.80, 0, 0.2])

        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Intensity ()')

        self.draw()

    def rad1click(self, data_plt, channel):
        #filtfilt - zero-phase filter
        self.figure.clear()
        self.my_channel = channel
        self.data = data_plt

        ax = self.figure.add_subplot(111)
        ax.autoscale(enable=True, axis='x', tight=bool)

        row = data_plt.shape[0]
        col = data_plt.shape[1]
        data_plt = data_plt[:, 7:col]

        r = data_plt[:, 149]
        s = np.arange(0, row, 1)

        a = 1
        n = 300
        b = [1.0 / n] * n
        f = signal.filtfilt(b, a, r)
        ax.plot(s, r, linewidth=0.5, c=[0.80, 0, 0.2])
        ax.plot(s, f, linewidth=2.0, c='b')

        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Intensity ()')

        self.draw()

    def rad2click(self, data_plt, channel):
        #Savitzky-Golay filter
        self.figure.clear()
        self.my_channel = channel
        self.data = data_plt

        ax = self.figure.add_subplot(111)
        ax.autoscale(enable=True, axis='x', tight=bool)

        row = data_plt.shape[0]
        col = data_plt.shape[1]
        data_plt = data_plt[:, 7:col]

        r = data_plt[:, 149]
        s = np.arange(0, row, 1)

        sg = signal.savgol_filter(r, 501, 2)
        ax.plot(s, r, linewidth=0.5, c=[0.80, 0, 0.2])
        ax.plot(s, sg, linewidth=2.0, c='g')

        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Intensity ()')

        self.draw()

    # def rad3click(self, data_plt, channel):
    #     # median filter
    #     self.figure.clear()
    #     self.my_channel = channel
    #     self.data = data_plt
    #
    #     ax = self.figure.add_subplot(111)
    #     ax.autoscale(enable=True, axis='x', tight=bool)
    #
    #     row = data_plt.shape[0]
    #     col = data_plt.shape[1]
    #     data_plt = data_plt[:, 7:col]
    #
    #     r = data_plt[:, 149]
    #     s = np.arange(0, row, 1)
    #
    #     mf = signal.medfilt(r, win)
    #     ax.plot(s, r, linewidth=0.5, c=[0.80, 0, 0.2])
    #     ax.plot(s, mf, linewidth=2.0, c='g')
    #
    #     ax.set_xlabel('Time (s)')
    #     ax.set_ylabel('Intensity ()')
    #
    #     self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Filtrace()
    sys.exit(app.exec_())
