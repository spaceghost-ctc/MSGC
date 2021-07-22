import serial
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, Qt, pyqtSlot
from PyQt5.QtWidgets import QCompleter
from gWind import Ui_MainWindow
import sys
import serial.tools.list_ports
import time
from datetime import datetime
from SerialConn import SerialConn


class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setupUi(self)

        self.ports = serial.tools.list_ports.comports()
        self.portNames = []

        self.Board1Connected = False
        self.Board2Connected = False

        self.Board1 = None
        self.Board2 = None

        self.board1recthread = None
        self.board2recthread = None

        for port, desc, hwid in sorted(self.ports):
            self.comboBox.addItem(desc)
            self.portNames.append("{}".format(port))

        for port, desc, hwid in sorted(self.ports):
            self.comboBox_2.addItem(desc)
            self.portNames.append("{}".format(port))
        self.pushButton.clicked.connect(self.connected_board1())
        self.pushButton_2.clicked.connect(self.connected_board2())

    def connected_board1(self):
        if not self.Board1Connected and self.comboBox.currentIndex() != 0:
            self.Board1 = SerialConn(self.portNames[self.comboBox.currentIndex()], 9600)
            self.Board1Connected = True
        elif self.Board1Connected:
            print("Already connected to Board 1")
        else:
            print("Failed to connect to board 1")
        return

    def connected_board2(self):
        if not self.Board2Connected and self.comboBox_2.currentIndex() != 0:
            self.Board2 = SerialConn(self.portNames[self.comboBox_2.currentIndex()], 9600)
            self.Board2Connected = True
        elif self.Board2Connected:
            print("Already connected to Board 2")
        else:
            print("Failed to connect to board 2")
        return


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
