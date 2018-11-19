import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QSizePolicy, QPushButton,\
QFileDialog, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
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
        self.height = 560

        self.button1 = QPushButton('Open file', self)
        self.label1 = QLabel('Data channel', self)
        self.kanal = QLineEdit('', self)
        self.button2 = QPushButton('Next', self)

        self.hboxLayout = QHBoxLayout(self)

        self.data = ''

        self.initUI()

    def initUI(self):
              self.setWindowTitle(self.title)
              self.setGeometry(self.left, self.top, self.width, self.height)

              self.button1.setToolTip('Click to open data file')
              self.button1.move(15, 7)
              self.button1.resize(72, 26)
              self.button1.clicked.connect(self.file_fcn)

              self.label1.move(443, 501)
              self.label1.resize = (50, 27)

              self.kanal.setToolTip('Enter data channel')
              self.kanal.move(525, 500)
              self.kanal.resize(100, 30)

              self.button2.move(630, 501)
              self.button2.resize(75, 27)
              self.button2.clicked.connect(self.btn_fcn)

              self.hboxLayout.addWidget(self.label1)
              self.hboxLayout.addWidget(self.kanal)
              self.hboxLayout.addWidget(self.button2)

              self.fig = plt.Figure(figsize=(10, 8))
              self.axes = self.fig.add_subplot(111)
              self.canvas = FigureCanvas(self.fig)
              self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
              self.canvas.updateGeometry()
              self.canvas.move(15, 40)

              self.plotit(self.data)

              self.show()

    def file_fcn(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Otevřít soubor - zpracování XRD dat", "",
                                                        "Data Files (*.dat);;All Files (*)", options=options)
        if self.fileName:
            self.data = np.genfromtxt(self.fileName)

        self.show()
        self.plotit(self.data)

    def plotit(self,data):
        try:
            if data:
                row = self.data.shape[0]
                col = self.data.shape[1]
                self.data = data[:, 7:col]
                x = np.arange(0, col - 7, 1)
                y = np.arange(0, row, 1)

                ax = self.figure.gca(projection='3d')
                x, y = np.meshgrid(x, y)
                surf = ax.plot_surface(x, y, self.data, cmap=cm.gist_stern,
                               linewidth=0, antialiased=False, vmin=np.amin(self.data), vmax=np.amax(self.data))
                self.figure.colorbar(surf)

                ax.set_title(str(self.fileName))
                ax.set_xlabel('Temperature (°C)')
                ax.set_ylabel('Time (s)')
                ax.set_zlabel('Intensity ()')

                self.canvas.draw()


        except ValueError:

                self.canvas.draw()

    def btn_fcn(self):
        try:
            k = int(self.kanal.text())
        except ValueError:
            print("Not a number")
        self.my_channel = k
        print("Value: "+str(self.my_channel))
        #self.newWin()

    #def newWin(self, my_channel):
    #filterWin





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())