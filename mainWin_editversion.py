import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QSizePolicy, QPushButton,\
QFileDialog, QLabel, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,\
QSlider, QRadioButton, QButtonGroup, QFormLayout, QTabBar
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from scipy import signal


class App(QMainWindow):
    #  -------------- main window initialization ---------------
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'XRD data processing'
        self.width = 720
        self.height = 540

        self.layout = QVBoxLayout(self)

        self.button1 = QPushButton('Open file', self)
        self.label1 = QLabel('', self)

        self.tabs = QTabWidget(self)
        self.tab1 = QWidget()
        self.label2 = QLabel('Specify theta', self)
        self.kanal = QLineEdit('', self)
        self.button2 = QPushButton('Next', self)

        self.m = PlotCanvas(self, 710, 450)
        self.m.move(15, 40)
        self.tools = NavigationToolbar(self.m, self)
        self.tools.move(15, 500)
        self.tools.resize(400, 30)

        self.setStyleSheet("QMainWindow { background-color: rgb(253, 253, 253) }")

        self.initUI()

    #  ------------ main tab & window configuration -------------
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMaximumSize(720, 540)

        self.button1.setToolTip('Click to open data file')
        self.button1.move(5, 7)
        self.button1.resize(90, 26)
        self.button1.clicked.connect(self.file_fcn)

        self.button2.move(630, 501)
        self.button2.resize(75, 27)
        self.button2.clicked.connect(self.btn_fcn)
        self.button2.clicked.connect(self.newTab_fcn)

        self.label1.move(100, 6)
        self.label1.setText(" Current file:  None ")
        self.label1.setMinimumWidth(600)
        self.label1.setMaximumHeight(27)

        self.tabs.resize(710, 500)
        self.tabs.move(5, 38)
        self.tabs.addTab(self.tab1, "Main window")

        self.label2.move(430, 500)
        self.label2.resize = (48, 27)

        self.kanal.setToolTip('Enter theta value')
        self.kanal.move(525, 500)
        self.kanal.resize(100, 30)

        self.buttons = QWidget(self)
        self.buttons_layout = QHBoxLayout()
        self.buttons.setLayout(self.buttons_layout)
        self.buttons_layout.addWidget(self.tools)
        self.buttons_layout.addWidget(self.label2)
        self.buttons_layout.addWidget(self.kanal)
        self.buttons_layout.addWidget(self.button2)

        self.tab1.layout = QVBoxLayout()
        self.tab1.layout.addWidget(self.m)
        self.tab1.layout.addWidget(self.buttons)
        self.tab1.setLayout(self.tab1.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.tabs.tabCloseRequested.connect(self.closeTab)

        self.show()

    #  --------- load data from file (open file button) ------------
    def file_fcn(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Open data file - XDR data processing", "",
                                                       "Data Files (*.dat);;All Files (*)", options=options)
        if self.fileName:
            self.data = np.genfromtxt(self.fileName)
            self.label1.setText(" Current file:   " + str(self.fileName))
            self.show()
            self.m.threedee_plt(self.data)
        else:
            print("Error: File not selected")

    #  -------------- channel ---------------
    def btn_fcn(self):
        try:
            k = int(self.kanal.text())

        except ValueError:
            print("Not a number")

        self.my_channel = k

    #  -------------- New tab configuration ---------------
    def newTab_fcn(self, i):

        k = self.my_channel
        self.position1 = 21
        self.position2 = -99

        self.tab = QWidget()
        self.tabs.addTab(self.tab, "Theta:  "+str(k)+" °")

        self.tabs.setCurrentIndex(i)

        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)

        self.m2 = NewTabCanvas(self, 710, 450)
        self.m2.move(15, 40)

        self.tabtools = NavigationToolbar(self.m2, self)

        self.label0 = QLabel('Select data filter and its parameters', self)
        self.label0.resize(250, 26)
        self.label0.setFont(QFont("Sans Serif", 11))
        self.labelx = QLabel('Export to file', self)
        self.labelx.resize(150, 26)
        self.labelx.setFont(QFont("Sans Serif", 11))

        self.rad1 = QRadioButton("&Zero-phase")
        self.rad1.setChecked(False)
        self.rad1.toggled.connect(lambda: self.m2.rad1click(self.data, self.my_channel))
        self.rad2 = QRadioButton("&Savitzky-Golay")
        self.rad2.setChecked(False)
        self.rad2.toggled.connect(lambda: self.m2.rad2click(self.data, self.my_channel))
        self.rad3 = QRadioButton("&Median")
        self.rad3.setChecked(False)
        self.rad3.toggled.connect(lambda: self.m2.rad3click(self.data, self.my_channel, self.position1))
        self.rad4 = QRadioButton("&Exponential smoothing")
        self.rad4.setChecked(False)
        self.rad4.toggled.connect(lambda: self.m2.rad4click(self.data, self.my_channel, self.position2))

        self.slide1 = QSlider(Qt.Horizontal, self)
        self.slide1.setMaximumWidth(110)
        self.slide1.setMinimum(11)
        self.slide1.setMaximum(501)
        self.slide1.setToolTip('Win length: '+str(self.position1))
        self.slide1.setSingleStep(20)
        self.slide1.setTickInterval(50)
        self.slide1.setTickPosition(QSlider.TicksBelow)
        self.slide1.setFocusPolicy(Qt.StrongFocus)
        self.slide1.valueChanged[int].connect(lambda: self.slide1_fcn(self.data, self.my_channel, \
                                                                      self.position1))
        self.slide2 = QSlider(Qt.Horizontal)
        self.slide2.move(300, 472)
        self.slide2.setMaximumWidth(110)
        self.slide2.setMinimum(-99)
        self.slide2.setMaximum(-1)

        self.slide2.setSingleStep(1)
        self.slide2.setTickInterval(10)
        self.slide2.setTickPosition(QSlider.TicksBelow)
        self.slide2.setFocusPolicy(Qt.StrongFocus)
        self.slide2.setValue(self.position2)
        self.slide2.setToolTip('Alpha: '+str(-(self.position2/800)))
        self.slide2.valueChanged[int].connect(lambda: self.slide2_fcn(self.data, self.my_channel, \
                                                                      self.position2))
        self.b1 = QPushButton('Export data', self)
        self.b1.setToolTip('Click to save data to a text file')
        self.b1.move(510, 450)
        self.b1.resize(120, 54)
        self.b1.clicked.connect(lambda: self.b1_fcn(self.m2.dat))

        self.b3 = QPushButton('Save chart', self)
        self.b3.setToolTip('Click to save chart as an image')
        self.b3.move(510, 508)
        self.b3.resize(120, 54)
        self.b3.clicked.connect(lambda: self.b3_fcn(self.m2.figure))

        self.layout1 = QHBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QVBoxLayout()
        self.layout4 = QHBoxLayout()

        self.widget1 = QWidget(self)
        self.widget2 = QWidget(self)
        self.widget3 = QWidget(self)
        self.widget4 = QWidget(self)

        self.widget1.setLayout(self.layout1)
        self.widget2.setLayout(self.layout2)
        self.widget3.setLayout(self.layout3)
        self.widget4.setLayout(self.layout4)

        self.layout1.addWidget(self.rad1)
        self.layout2.addWidget(self.rad2)
        self.layout1.addWidget(self.rad3)
        self.layout2.addWidget(self.rad4)
        self.layout1.addWidget(self.slide1)
        self.layout2.addWidget(self.slide2)
        self.layout3.addWidget(self.labelx)
        self.layout3.addWidget(self.b1)
        self.layout3.addWidget(self.b3)
        self.layout4.addWidget(self.label0)

        self.group = QButtonGroup(self)
        self.group.addButton(self.rad1)
        self.group.addButton(self.rad2)
        self.group.addButton(self.rad3)
        self.group.addButton(self.rad4)

        self.tab.layout = QGridLayout(self)
        self.tab.layout.setSpacing(5)
        self.tab.layout.addWidget(self.m2, 1, 0, 4, 2)
        self.tab.layout.addWidget(self.widget1, 6, 0)
        self.tab.layout.addWidget(self.widget2, 7, 0)
        self.tab.layout.addWidget(self.widget4, 5, 0)
        self.tab.layout.addWidget(self.widget3, 5, 1, 3, 1)
        self.tab.layout.addWidget(self.tabtools, 8, 0, 1, 2)
        self.tab.setLayout(self.tab.layout)

        self.m2.twodee_plt(self.data, self.my_channel)

    #  -------------- export data to files functions ---------------
    def b1_fcn(self, cisla):
        try:
            self.m2.dat
        except NameError:
            print("Process data first")
        except ValueError:
            print("")
        else:
            self.m2.dat = cisla

        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "Data Files (*.csv);;All files (*)")
        if fileName:
            d = cisla.shape[0]
            x = np.arange(0, d, 1)
            data = np.column_stack((x, cisla))
            head = "Time (s), Intensity ()"
            np.savetxt(fileName, data, header=head, delimiter=',')
        else:
            print("Error: File not saved")

    def b3_fcn(self, fig):
        self.m2.figure = fig
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "Image files (*.jpg);;Portable Graphics (*.png)"
                                                  ";;Vector Graphics (*.svg);;PDF files (*.pdf);;All Files (*)")
        suffix = fileName[-3:]
        if not fileName:
            print("Error: File not saved")
        if fileName:
            fig.savefig(fname=fileName, format=suffix)

    #  -------------- median filter slider ---------------
    def slide1_fcn(self, data, channel, position):
        self.position1 = position
        self.data = data
        self.my_channel = channel
        position = self.slide1.value()
        self.position1 = position
        self.m2.rad3click(self.data, self.my_channel, self.position1)
        self.slide1.setToolTip('Win length: '+str(self.position1))

    #  -------------- exponential smoothing slider ---------------
    def slide2_fcn(self, data, channel, position):
        self.position2 = position
        self.data = data
        self.my_channel = channel
        position = self.slide2.value()
        self.position2 = position
        self.m2.rad4click(self.data, self.my_channel, self.position2)
        self.slide2.setToolTip('Alpha: '+str(-(position/800)))

    def closeTab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)


#  -------------- figure canvas for the main tab ---------------
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=710, height=500):
        fig = Figure(figsize=(710, 500))
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def threedee_plt(self, data_plt):
        self.data = data_plt
        ax = self.figure.add_subplot(111)
        ax.plot(data_plt)
        ax.autoscale(enable=True, axis='x, y', tight=bool)
        row = data_plt.shape[0]
        col = data_plt.shape[1]
        data_plt = data_plt[:, 7:col]
        x = np.arange(0, col - 7, 1)
        y = np.arange(0, row, 1)

        ax = self.figure.gca(projection='3d')
        x, y = np.meshgrid(x, y)
        surf = ax.plot_surface(x, y, data_plt, cmap=cm.gist_stern, linewidth=0, antialiased=False,\
                               vmin=np.amin(data_plt), vmax=np.amax(data_plt))

        self.figure.colorbar(surf)

        ax.set_xlabel('Theta (deg)')
        ax.set_ylabel('Time (s)')
        ax.set_zlabel('Intensity ()')

        self.draw()


#  -------------- figure canvas for newly open tabs ---------------
class NewTabCanvas(FigureCanvas):
    def __init__(self, parent=None, width=710, height=500):
        fig2 = Figure(figsize=(710, 500))
        self.axes = fig2.add_subplot(111)

        FigureCanvas.__init__(self, fig2)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def twodee_plt(self, data_plt, kanal):
        self.my_channel = kanal
        self.data = data_plt
        ax = self.figure.add_subplot(111)
        ax.autoscale(enable=True, axis='x', tight=bool)

        row = data_plt.shape[0]
        col = data_plt.shape[1]
        data_plt = data_plt[:, 7:col]

        r = data_plt[:, kanal]
        s = np.arange(0, row, 1)

        ax.plot(s, r, linewidth=0.5, c=[0.80, 0, 0.2])

        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Intensity ()')

    # -------- filtfilt - zero-phase filter -----------
    def rad1click(self, data_plt, channel):

        self.figure.clear()
        self.my_channel = channel
        self.data = data_plt

        ax = self.figure.add_subplot(111)
        ax.autoscale(enable=True, axis='x', tight=bool)

        row = data_plt.shape[0]
        col = data_plt.shape[1]
        data_plt = data_plt[:, 7:col]

        r = data_plt[:, channel]
        s = np.arange(0, row, 1)

        a = 1
        n = 50
        b = [1.0/n]*n

        f = signal.filtfilt(b, a, r)
        ax.plot(s, r, linewidth=0.5, c=[0.80, 0, 0.2])
        ax.plot(s, f, linewidth=2.0, c=[0.251, 0.878, 0.816])

        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Intensity ()')

        self.dat = f

        self.draw()

    # ------------ Savitzky-Golay filter ------------
    def rad2click(self, data_plt, channel):

        self.figure.clear()
        self.my_channel = channel
        self.data = data_plt
        ax = self.figure.add_subplot(111)
        ax.autoscale(enable=True, axis='x', tight=bool)

        row = data_plt.shape[0]
        col = data_plt.shape[1]
        data_plt = data_plt[:, 7:col]

        r = data_plt[:, channel]
        s = np.arange(0, row, 1)
        sg = signal.savgol_filter(r, 301, 5)
        ax.plot(s, r, linewidth=0.5, c=[0.80, 0, 0.2])
        ax.plot(s, sg, linewidth=2.0, c=[0.196, 0.804, 0.196])

        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Intensity ()')

        self.dat = sg

        self.draw()

    # ------------- median filter ---------------
    def rad3click(self, data_plt, channel, win):

        self.figure.clear()
        self.position1 = win
        self.my_channel = channel
        self.data = data_plt

        ax = self.figure.add_subplot(111)
        ax.autoscale(enable=True, axis='x', tight=bool)

        row = data_plt.shape[0]
        col = data_plt.shape[1]
        data_plt = data_plt[:, 7:col]

        r = data_plt[:, channel]
        s = np.arange(0, row, 1)

        mf = np.zeros(len(s))
        for i in range(len(s)):
            k = (win - 1) // 2
            q = r[i + 1:((i + 1) + k)]
            n = r[(i - k):i]
            u = r[i + 1:i + (k - i) + 1]
            if i < k:  # left boundaries
                a = np.concatenate((u[::-1], r[:i + 1], q), axis=None)
                mf[i] = np.median(a)
            elif (i + ((win - 1) // 2)) > (len(s) - 1):  # right boundaries
                p = r[i - k:i - (len(s) - 1 - i)]
                b = np.concatenate((n, r[i:], p[::-1]), axis=None)
                mf[i] = np.median(b)
            else:  # middle data
                c = r[i - ((win - 1) // 2):(i + ((win + 1) // 2))]
                mf[i] = np.median(c)

        ax.plot(s, r, linewidth=0.5, c=[0.80, 0, 0.2])
        ax.plot(s, mf, linewidth=2.0, c=[1, 1, 0])
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Intensity ()')
        self.dat = mf

        self.draw()

    # ---------- exponential moving average -----------
    def rad4click(self, data_plt, channel, alpha):

        self.figure.clear()
        self.my_channel = channel
        self.data = data_plt
        self.position2 = alpha

        alpha = -(alpha/800)

        ax = self.figure.add_subplot(111)
        ax.autoscale(enable=True, axis='x', tight=bool)

        row = data_plt.shape[0]
        col = data_plt.shape[1]
        data_plt = data_plt[:, 7:col]

        r = data_plt[:, channel]
        s = np.arange(0, row, 1)

        aux = np.zeros(r.shape)

        for idx, a in np.ndenumerate(r):
            if idx[0] == 0:
                aux[idx[0]] = a
            else:
                aux[idx[0]] = alpha * a + (1 - alpha) * aux[idx[0] - 1]

        ax.plot(s, r, linewidth=0.5, c=[0.80, 0, 0.2])
        ax.plot(s, aux, linewidth=2.0, c=[1, 0, 0])

        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Intensity ()')

        self.dat = aux

        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
