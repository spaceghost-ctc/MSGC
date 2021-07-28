import serial

class SerialConn:

    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.COM_Port = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=.1)
        self.DataPack = []
        self.attempt_num = 0
        self.sensor_data = []
        return
