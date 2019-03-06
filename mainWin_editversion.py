import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QSizePolicy, QPushButton,\
QFileDialog, QLabel, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,\
QSlider, QRadioButton, QButtonGroup, QFormLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


class App(QMainWindow):
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

        self.initUI()

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
        self.tabs.addTab(self.tab1, " Main ")

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

        self.show()

    def file_fcn(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Otevřít soubor - zpracování XRD dat", "",
                                                       "Data Files (*.dat);;All Files (*)", options=options)
        if self.fileName:
            self.data = np.genfromtxt(self.fileName)
            self.label1.setText(" Current file:   " + str(self.fileName))
            self.show()
            self.m.threedee_plt(self.data)
        else:
            print("Error: File not selected")

    def btn_fcn(self):
        try:
            k = int(self.kanal.text())

        except ValueError:
            print("Not a number")

        self.my_channel = k

    def newTab_fcn(self):
        k = self.my_channel
        self.tab = QWidget()
        self.tabs.addTab(self.tab, "Theta:  "+str(k)+" °")
        self.tabs.setTabsClosable(True)

        self.m2 = NewTabCanvas(self, 710, 450)
        self.m2.move(15, 40)

        self.label0 = QLabel('Select data filter and its parameters', self)
        self.label0.setFont(QFont("Sans Serif", 11))
        self.labelx = QLabel('Export to file', self)
        self.labelx.setFont(QFont("Sans Serif", 11))

        self.rad1 = QRadioButton("&Zero-phase")
        self.rad1.setChecked(False)
        self.rad2 = QRadioButton("&Savitzky-Golay")
        self.rad2.setChecked(False)
        self.rad3 = QRadioButton("&Median")
        self.rad3.setChecked(False)
        self.rad4 = QRadioButton("&Exponential smoothing")
        self.rad4.setChecked(False)

        self.slide1 = QSlider(Qt.Horizontal, self)
        self.slide1.setMaximumWidth(110)
        self.slide1.setMinimum(11)
        self.slide1.setMaximum(501)
        self.slide1.setToolTip('Window length')
        self.slide1.setSingleStep(10)
        self.slide1.setTickInterval(50)
        self.slide1.setTickPosition(QSlider.TicksBelow)
        self.slide1.setFocusPolicy(Qt.StrongFocus)

        self.slide2 = QSlider(Qt.Horizontal)
        self.slide2.move(300, 472)
        self.slide2.setMaximumWidth(110)
        self.slide2.setMinimum(0)
        self.slide2.setMaximum(1.0)
        self.slide2.setToolTip('Parameter alpha')
        self.slide2.setSingleStep(.05)
        self.slide2.setTickInterval(.1)
        self.slide2.setTickPosition(QSlider.TicksBelow)
        self.slide2.setFocusPolicy(Qt.StrongFocus)

        self.b1 = QPushButton('Save data as .csv', self)
        self.b1.setToolTip('Click to save data to .csv file')
        self.b1.move(510, 450)
        self.b1.resize(120, 27)

        self.b2 = QPushButton('Save data as .xls', self)
        self.b2.setToolTip('Click to save data to .xls file')
        self.b2.move(510, 479)
        self.b2.resize(120, 27)

        self.b3 = QPushButton('Save chart as .png', self)
        self.b3.setToolTip('Click to save chart as .png')
        self.b3.move(510, 508)
        self.b3.resize(120, 27)

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

        self.widget1.resize(440, 35)
        self.widget1.move(10, 440)
        self.widget2.resize(440, 35)
        self.widget2.move(10, 468)
        self.widget3.move(520, 450)
        self.widget3.resize(120, 90)
        self.widget4.move(15,412)
        self.widget4.resize(720, 27)

        self.layout1.addWidget(self.rad1)
        self.layout2.addWidget(self.rad2)
        self.layout1.addWidget(self.rad3)
        self.layout2.addWidget(self.rad4)
        self.layout1.addWidget(self.slide1)
        self.layout2.addWidget(self.slide2)
        self.layout3.addWidget(self.labelx)
        self.layout3.addWidget(self.b1)
        self.layout3.addWidget(self.b2)
        self.layout3.addWidget(self.b3)
        self.layout4.addWidget(self.label0)

        self.group = QButtonGroup(self)
        self.group.addButton(self.rad1)
        self.group.addButton(self.rad2)
        self.group.addButton(self.rad3)
        self.group.addButton(self.rad4)

        self.tab.layout = QGridLayout(self)
        self.tab.layout.setSpacing(7)
        self.tab.layout.addWidget(self.m2, 1, 0, 4, 2)
        self.tab.layout.addWidget(self.widget1, 6, 0)
        self.tab.layout.addWidget(self.widget2, 7, 0)
        self.tab.layout.addWidget(self.widget4, 5, 0)
        self.tab.layout.addWidget(self.widget3, 5, 1, 3, 1)
        self.tab.setLayout(self.tab.layout)

        # ----------- debugger ------------------------------
        print(self.data.shape) # funkční
        print(str(self.my_channel)) # funkční
        # tady chyba:
        #self.m2.twodee_plt(self.data, self.my_channel)
        print("ok2") # nepotvrzeno
        # ---------------------------------------------------

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
        surf = ax.plot_surface(x, y, data_plt, cmap=cm.gist_stern, linewidth=0, antialiased=False, vmin=np.amin(data_plt), vmax=np.amax(data_plt))

        self.figure.colorbar(surf)

        ax.set_xlabel('Theta (deg)')
        ax.set_ylabel('Time (s)')
        ax.set_zlabel('Intensity ()')

        self.draw()


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

        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())