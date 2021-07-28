import serial
import serial.tools.list_ports
import tkinter as tk
import sys

from gWind import Ui_mainWindow
from lora_serial import SerialConn


class Window(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)

        self.ports = serial.tools.list_ports.comports()
        self.portNames = []

        self.board_connected = False
        self.running = False
        self.connect_board = None
        self.start_run = None
        self.stop_run = None
        self.worker = None
        self.board = None
        self.board_thread = None

        for port, desc, hwid in sorted(self.ports):
            self.board_port.addItem(desc)
            self.portNames.append("{}".format(port))  #  WORKS TO HERE

        self.board_select.clicked.connect(self.connect_board)

    def connect_board(self):
        if not self.board_connected and self.board_port.currentIndex() != 0:
            self.board = SerialConn(self.portNames[self.board_port.currentIndex()], 9600)
            self.board_connected = True
            print("Board Connected")
            self.start_button.setEnabled(True)
        elif self.board_connected:
            print("Board Already Connected")
        else:
            print("Failed to Connect")
        return


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Window()
    MainWindow.show()

    sys.exit(app.exec_())
