import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QSizePolicy, QPushButton,\
QFileDialog, QLabel

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
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
        self.height = 560

        self.kanal=QLineEdit('',self)
        self.moje_promenna = "neco"
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        m = PlotCanvas(self, width=6.9, height=4.5)
        m.move(15, 40)

        self.kanal.setToolTip('Enter data channel')
        self.kanal.move(525, 500)
        self.kanal.resize(100, 30)

        button1=QPushButton('Open file', self)
        button1.setToolTip('Click to open data file')
        button1.move(15,7)
        button1.resize(72,26)
        button1.clicked.connect(self.file_fcn)

        label1=QLabel('Data channel',self)
        label1.move(443,501)
        label1.resize=(50,27)



        button2 = QPushButton('Next', self)
        button2.move(630,501)
        button2.resize(75,27)
        button2.clicked.connect(self.btn_fcn)

        self.show()

        
    def file_fcn(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Otevřít soubor - zpracování XRD dat", "",
                                                  "Data Files (*.dat);;All Files (*)", options=options)
        if fileName:
           data = np.genfromtxt(fileName)
           print(data.shape)
        self.show()

    def btn_fcn(self):
        try:
            k =int(self.kanal.text())
            print(k)
        except ValueError:
            print("not a number")
        self.moje_promenna = "neco jinyho"
        print(self.moje_promenna)


        
class PlotCanvas(FigureCanvas):

        def __init__(self, parent=None, width=10, height=8, dpi=100):

            fig = Figure(figsize=(width, height), dpi=dpi)
            self.axes = fig.add_subplot(111)

            FigureCanvas.__init__(self, fig)
            self.setParent(parent)

            FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
            FigureCanvas.updateGeometry(self)
            self.plot()
            

        def plot(self):
               import os
               #os.chdir('F:\\')
               data = np.genfromtxt('testovaci.dat',delimiter='\t')
               row = data.shape[0]
               col = data.shape[1]
               data = data[:, 7:col]
               x = np.arange(0, col - 7, 1)
               y = np.arange(0, row, 1)
               ax = self.figure.gca(projection='3d')
               ax.set_title('filename.dat')

               x, y = np.meshgrid(x, y)
               surf = ax.plot_surface(x, y, data, cmap=cm.gist_stern,
                                      linewidth=0, antialiased=False, vmin=np.amin(data), vmax=np.amax(data))
               self.figure.colorbar(surf)

               self.draw()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
