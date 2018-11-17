import sys
from PyQt5.QtWidgets import QWidget, QFileDialog, QApplication
from matplotlib import numpy as np

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):

        self.setGeometry(self.left, self.top, self.width, self.height)

        self.openFileNameDialog()

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Otevřít soubor - zpracování XRD dat", "",
                                                  "Data Files (*.dat);;All Files (*)", options=options)
        if fileName:
            data=np.genfromtxt(fileName)
            print(data.shape)
        QFileDialog(exit())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())