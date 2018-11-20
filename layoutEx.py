import sys
import PyQt5
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider


class Class1(QMainWindow):
    def __init__(self):
        super(Class1, self).__init__()
        self.func()

    def func(self):
        layout = PyQt5.QtWidgets.QHBoxLayout()  # layout for the central widget
        widget = PyQt5.QtWidgets.QWidget(self)  # central widget
        widget.setLayout(layout)

        number_group = PyQt5.QtWidgets.QButtonGroup(widget)  # Number group
        r0 = PyQt5.QtWidgets.QRadioButton("0")
        number_group.addButton(r0)
        r1 = PyQt5.QtWidgets.QRadioButton("1")
        number_group.addButton(r1)
        layout.addWidget(r0)
        layout.addWidget(r1)

        letter_group = PyQt5.QtWidgets.QButtonGroup(widget)  # Letter group
        ra = PyQt5.QtWidgets.QRadioButton("a")
        letter_group.addButton(ra)
        rb = PyQt5.QtWidgets.QRadioButton("b")
        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(10)
        slider.setSingleStep(1)
        letter_group.addButton(rb)
        layout.addWidget(ra)
        layout.addWidget(rb)
        layout.addWidget(slider)
        # assign the widget to the main window
        self.setCentralWidget(widget)
        self.show()



def main():
    app = QApplication(sys.argv)
    mw = Class1()
    mw.show()
    sys.exit(app.exec_())


if __name__=='__main__':
    main()
