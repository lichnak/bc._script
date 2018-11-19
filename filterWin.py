import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QSizePolicy, QPushButton,\
QFileDialog, QLabel, QRadioButton, QSlider
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

#import filterWin ...externi okno pro filtraci dat ve vybranem kanalu

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'XRD data processing'
        self.width = 720
        self.height = 550

        self.m = PlotCanvas(self, width=7.05, height=4)
        self.m.move(7, 7)
        self.tools = NavigationToolbar(self.m, self)
        self.tools.move(7, 513)
        self.tools.resize(415, 30)

        self.label0 = QLabel('Select data filter and parameters', self)
        self.label1 = QLabel('Zero-phase', self)
        self.rad1 = QRadioButton("Radio zero-phase filter")
        self.label2 = QLabel('Savitzky-Golay', self)
        self.rad2 = QRadioButton("Radio Savitzky-Golay filter")
        self.label3 = QLabel('Median', self)
        self.rad3 = QRadioButton("Radio median filter")
        self.label4 = QLabel('Exponential', self)
        self.rad4 = QRadioButton("Radio exponential smoothing filter")
        self.slide1 = QSlider()
        self.slide2 = QSlider()

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label0.move(15, 412)
        self.label0.resize(250, 26)
        self.label0.setFont(QFont("Sans Serif", 11))

        self.label1.move(40, 441)
        self.label1.resize(80, 26)
        self.rad1.move(15, 441)
        self.rad1.setChecked(False)

        self.label2.move(40, 472)
        self.label2.resize(80, 26)
        self.rad2.move(15, 472)
        self.rad2.setChecked(False)

        self.label3.move(200, 441)
        self.label3.resize(80, 26)
        self.rad3.move(170, 441)
        self.rad3.setChecked(False)
        self.slide1.move(300, 441)
        self.slide1.setRange(9, 999)
        self.slide1.setToolTip('Window length')
        self.slide1.setSingleStep(1)
        self.slide1.setTickInterval(100)
        self.slide1.setTickPosition(QSlider.TicksBelow)
        self.slide1.setFocusPolicy(Qt.StrongFocus)
        
        self.label4.move(200, 472)
        self.label4.resize(80, 26)
        self.rad4.move(170, 472)
        self.rad4.setChecked(True)
        self.slide2.move(300, 472)
        self.slide2.setRange(0, 99)
        self.slide2.setToolTip('Alpha parameter')
        self.slide2.setSingleStep(1)
        self.slide2.setTickInterval(10)
        self.slide2.setTickPosition(QSlider.TicksBelow)
        self.slide2.setFocusPolicy(Qt.StrongFocus)

        self.show()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=7.05, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)



#     def plotit(self, data_plt):
#         self.data = data_plt
#         ax = self.figure.add_subplot(111)
#         ax.plot(data_plt)
#         row = data_plt.shape[0]
#         col = data_plt.shape[1]
#         data_plt = data_plt[:, 7:col]
#         x = np.arange(0, col - 7, 1)
#         y = np.arange(0, row, 1)

#         ax = self.figure.gca(projection='3d')
#         x, y = np.meshgrid(x, y)
#         surf = ax.plot_surface(x, y, data_plt, cmap=cm.gist_stern, linewidth=0, antialiased=False, vmin=np.amin(data_plt), vmax=np.amax(data_plt))

#         self.figure.colorbar(surf)


#         ax.set_xlabel('Theta (° )')
#         ax.set_ylabel('Time (s)')
#         ax.set_zlabel('Intensity ()')

#         self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
