import serial
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, Qt, pyqtSlot, pyqtBoundSignal
from PyQt5.QtWidgets import QCompleter
from gWind import Ui_mainWindow
import sys
import serial.tools.list_ports
import time
from datetime import datetime
from SerialConn import SerialConn


#  TODO: Fix the Worker threads
#  TODO: Display Data from Threads
#  TODO: .csv output files
#  TODO: Graphic Outputs
#  TODO: Single Board Option


class Window(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)

        self.ports = serial.tools.list_ports.comports()
        self.portNames = []

        self.Board1Connected = False
        self.Board2Connected = False

        self.running = False

        self.run = None
        self.stop_run = None

        self.worker1 = None
        self.worker2 = None
        self.Board1 = None
        self.Board2 = None

        self.board1recthread = None
        self.board2recthread = None

        #  Data from LoRa

        self.data_pack1 = 0
        self.data_pack2 = 0

        self.BoardID = ''
        self.Temp1 = 0
        self.Temp2 = 0
        self.Temp3 = 0
        self.Pressure = 0
        self.X = 0
        self.Y = 0
        self.Z = 0
        self.sent = 0
        self.received = 0
        self.TIME = 0
        self.LAT = 0
        self.LON = 0
        self.ALT = 0

        for port, desc, hwid in sorted(self.ports):
            self.board_1_port.addItem(desc)
            self.portNames.append("{}".format(port))

        for port, desc, hwid in sorted(self.ports):
            self.board_2_port.addItem(desc)
            self.portNames.append("{}".format(port))

        self.board_1_select_port.clicked.connect(self.connected_board1)
        self.board_2_select_port.clicked.connect(self.connected_board2)

        self.running_start.clicked.connect(self.start_check)
        self.running_stop.clicked.connect(lambda: self.stop_run) #  NOT THE ANSWER, STILL NOT WORKING

    def connected_board1(self):
        if not self.Board1Connected and self.board_1_port.currentIndex() != 0:
            self.Board1 = SerialConn(self.portNames[self.board_1_port.currentIndex()], 9600)
            self.Board1Connected = True
            if self.Board2Connected:
                self.running_label.setPlainText("Ready To Run, Press START")
            else:
                self.running_label.setPlainText("Setup Board 2")
        elif self.Board1Connected:
            print("Already connected to Board 1")
        else:
            print("Failed to connect to board 1")
        return

    def connected_board2(self):
        if not self.Board2Connected and self.board_2_port.currentIndex() != 0:
            self.Board2 = SerialConn(self.portNames[self.board_2_port.currentIndex()], 9600)
            self.Board2Connected = True
            if self.Board1Connected:
                self.running_label.setPlainText("Ready To Run, Press START")
            else:
                self.running_label.setPlainText("Setup Board 1")
        elif self.Board2Connected:
            print("Already connected to Board 2")
        else:
            print("Failed to connect to board 2")
        return

    def start_check(self):
        if self.Board1Connected:
            print("Board 1 Ready")
        else:
            print("Board 1 Not Connected")
        if self.Board2Connected:
            print("Board 2 Ready")
        else:
            print("Board 2 Not Connected")

        if self.Board1Connected and self.Board2Connected:
            print("Starting System")
            self.running_label.setPlainText("System Running")
            self.running_start.setEnabled(False)
            self.running_stop.setEnabled(True)
            self.run()
            return True
        else:
            return False

    def run(self):
        self.running = True

    def stop_run(self):
        if self.running:
            self.Board1Connected = False
            self.Board2Connected = False
            self.Board1 = None
            self.Board2 = None
            self.running = False
            self.running_start.setEnabled(True)
            self.running_stop.setEnabled(False)
            self.running_label.setPlainText("System Stopped, Reset Connections")
            return True
        else:
            return False

#     def run(self):
#         self.running = True
#         self.board1recthread = QThread()
#         self.board2recthread = QThread()
#         self.worker1 = Worker1()
#         self.worker2 = Worker2()
#
#         self.worker1.moveToThread(self.board1recthread)
#         self.board1recthread.started.connect(self.worker1.running)
#
#         self.worker2.moveToThread(self.board2recthread)
#         self.board2recthread.started.connect(self.worker2.running)
#
#         self.worker1.finished.connect(self.run.quit)  # pycharm bug
#         self.worker2.finished.connect(self.run.quit)
#         self.worker1.finished.connect(self.worker1.deleteLater)
#         self.worker2.finished.connect(self.worker2.deleteLater)
#         self.board1recthread.finished.connect(self.board1recthread.deleteLater)
#         self.board2recthread.finished.connect(self.board2recthread.deleteLater)
#
#
# class Worker1(QObject):
#     finished = pyqtSignal()
#     calcSignal = pyqtSignal(str, float, float, float, float, float,
#                             float, float, float, float, float, float,
#                             float, float)
#
#     i = 0
#
#     def run(self):
#         if MainWindow.Board1Connected:
#             data_in = MainWindow.Board1.rec_data_pack()
#             print(data_in)
#             self.calcSignal.connect(MainWindow.data_pack1)
#             self.calcSignal.emit('', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
#         self.finished.emit()
#         return
#
#
# class Worker2(QObject):
#     finished = pyqtSignal()
#     calcSignal = pyqtSignal(str, float, float, float, float, float,
#                             float, float, float, float, float, float,
#                             float, float)
#
#     i = 0
#
#     def run(self):
#         if MainWindow.Board2Connected:
#             data_in = MainWindow.Board2.rec_data_pack()
#             print(data_in)
#             self.calcSignal.connect(MainWindow.data_pack2)
#             self.calcSignal.emit('', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
#         self.finished.emit()
#         return


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Window()
    MainWindow.show()

    sys.exit(app.exec_())
