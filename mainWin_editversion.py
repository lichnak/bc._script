import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QSizePolicy, QPushButton,\
QFileDialog, QLabel, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,\
QSlider, QRadioButton, QButtonGroup, QFormLayout
from PyQt5.QtCore import Qt, pyqtSignal

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
            self.m.plotit(self.data)
        else:
            print("Error: File not selected")

    def btn_fcn(self):
        try:
            k = int(self.kanal.text())
            print("ok4")

        except ValueError:
            print("Not a number")

        self.my_channel = k

    def newTab_fcn(self):
        k = self.my_channel
        self.tab = QWidget()
        self.tabs.addTab(self.tab, "Theta:  "+str(k)+" °")
        self.tabs.setTabsClosable(True)

        self.m2 = PlotCanvas(self, 710, 450)
        self.m2.move(15, 40)

        self.label0 = QLabel('Select data filter and its parameters', self)
        self.labelx = QLabel('Export to file', self)
        self.rad1 = QRadioButton("&Zero-phase")
        self.rad2 = QRadioButton("&Savitzky-Golay")
        self.rad3 = QRadioButton("&Median")
        self.rad4 = QRadioButton("&Exponential smoothing")
        self.slide1 = QSlider(Qt.Horizontal, self)
        self.slide2 = QSlider(Qt.Horizontal)
        self.b1 = QPushButton('Save data as .csv', self)
        self.b2 = QPushButton('Save data as .xls', self)
        self.b3 = QPushButton('Save chart as .png', self)

        self.layout1 = QHBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QVBoxLayout()

        self.widget1 = QWidget(self)
        self.widget2 = QWidget(self)
        self.widget3 = QWidget(self)
        self.widget1.setLayout(self.layout1)
        self.widget2.setLayout(self.layout2)
        self.widget3.setLayout(self.layout3)
        self.widget1.resize(440, 35)
        self.widget1.move(10, 440)
        self.widget2.resize(440, 35)
        self.widget2.move(10, 468)
        self.widget3.move(520, 450)
        self.widget3.resize(120, 90)

        self.layout1.addWidget(self.rad1)
        self.layout2.addWidget(self.rad2)
        self.layout1.addWidget(self.rad3)
        self.layout2.addWidget(self.rad4)
        self.layout1.addWidget(self.slide1)
        self.layout2.addWidget(self.slide2)
        self.layout3.addWidget(self.b1)
        self.layout3.addWidget(self.b2)
        self.layout3.addWidget(self.b3)

        self.group = QButtonGroup(self)
        self.group.addButton(self.rad1)
        self.group.addButton(self.rad2)
        self.group.addButton(self.rad3)
        self.group.addButton(self.rad4)

        self.tab.layout = QGridLayout(self)
        self.tab.layout.addWidget(self.m2, 0, 0, 4, -1)
        self.tab.layout.addWidget(self.widget1, 4, 0, 2, 1)
        self.tab.layout.addWidget(self.widget2, 5, 0, 2, 1)
        self.tab.layout.addWidget(self.widget3, 4, 6, 1, -1)
        self.tab.setLayout(self.tab.layout)


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

    def plotit(self, data_plt):
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
