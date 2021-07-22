import serial
import serial.tools.list_ports
import numpy as np


class SerialConn:

    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.COM_Port = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=.1)
        self.DataPack = []
        self.attempt_num = 0
        self.sensor_data = []
        return

    def data_rec(self):
        self.DataPack = self.rec_data_pack()
        return self.DataPack

    def rec_data_pack(self):
        if self.attempt_num < 100:
            self.attempt_num += 1
            char = self.COM_Port.read().decode("utf-8")
            string_rec = char
            self.sensor_data[12] = self.sensor_data[12] + 1
            self.DataPack = np.asarray(string_rec.split(','))
            print(self.DataPack)
        return self.DataPack
