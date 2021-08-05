import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import *
from tkinter import ttk
import threading
import numpy as np
import csv
from datetime import datetime
import os

#  TODO: 2s Comp on Temp P <2021.8.5> -L [Modified First 5 Packet Calculations]
#  TODO: GPS Parse Fix
#  TODO: Packet Counter Fix
#  TODO: Board ID Print Terminal
#  TODO: Useful NEMO Data Display
#  TODO: Decimal Rounding
#  TODO: Accel to m/s2
#  TODO: NEMO Packet Loss


class Window(object):
    def __init__(self):
        self.thread2 = None
        self.thread1 = None
        self.frame = None
        self.board = None
        self.board2 = None
        self.ports = serial.tools.list_ports.comports()
        self.portNames = []
        self.data_stream = ""
        self.data_packet = []

        self.board_connected = False
        self.i2c_connected = False
        self.running = False

        self.two_board_mode = False
        self.board_connected2 = False
        self.i2c_connected2 = False
        self.running2 = False

        for port, desc, hwid in sorted(self.ports):
            self.portNames.append("{}".format(port))

        self.start_select = None
        self.stop_select = None
        self.add_button = None

        self.com_list = None
        self.sel_i2c_list = None
        self.i2c_type = None
        self.run_b1_thread = None

        self.com_list2 = None
        self.sel_i2c_list2 = None
        self.i2c_type2 = None
        self.run_b1_thread2 = None

        self.board_val = None
        self.time_val = None
        self.lat_val = None
        self.lon_val = None
        self.altm_val = None
        self.altft_val = None
        self.temp1_val = None
        self.temp2_val = None
        self.tempp_val = None
        self.press_val = None
        self.x_val = None
        self.y_val = None
        self.z_val = None
        self.pack_s_val = None
        self.pack_r_val = None
        self.pack_l_val = None

        self.board_val2 = None
        self.time_val2 = None
        self.lat_val2 = None
        self.lon_val2 = None
        self.altm_val2 = None
        self.altft_val2 = None
        self.temp1_val2 = None
        self.temp2_val2 = None
        self.tempp_val2 = None
        self.press_val2 = None
        self.x_val2 = None
        self.y_val2 = None
        self.z_val2 = None
        self.pack_s_val2 = None
        self.pack_r_val2 = None
        self.pack_l_val2 = None

        self.nemo_data_val = None
        self.nemo_hist_val = None
        self.nemo_data_val2 = None
        self.nemo_hist_val2 = None

    def setup_ui(self, main_window):
        main_window.title("LoRa UI v5")
        main_window.geometry('800x800')
        self.frame = Frame(main_window, padx=5, pady=5)
        self.frame.pack(expand=True)

        com_list_label = Label(self.frame, text="Board Port")
        com_list_label.grid(row=0, column=1)
        self.com_list = ttk.Combobox(self.frame, values=self.portNames)
        self.com_list.grid(row=0, column=2)
        com_select = Button(self.frame, text="Select", command=self.connect_board)
        com_select.grid(row=0, column=3)

        self.add_button = Button(self.frame, text="+", command=self.add_board)
        self.add_button.grid(row=0, column=4)

        sel_i2c_label = Label(self.frame, text="I2C Addition")
        sel_i2c_label.grid(row=1, column=1)
        self.sel_i2c_list = ttk.Combobox(self.frame, values=["None", "NEMO"])
        self.sel_i2c_list.grid(row=1, column=2)
        sel_i2c_select = Button(self.frame, text="Select", command=self.connect_i2c)
        sel_i2c_select.grid(row=1, column=3)

        self.start_select = Button(self.frame, text="START", command=self.ready_check)
        self.start_select.grid(row=2, column=3)

        self.stop_select = Button(self.frame, text="STOP", command=self.sys_stop)
        self.stop_select.grid(row=2, column=4)
        self.stop_select["state"] = DISABLED

        board_label = Label(self.frame, text="Board ID")
        board_label.grid(row=4, column=1)
        self.board_val = Label(self.frame, text="")
        self.board_val.grid(row=4, column=2)

        time_label = Label(self.frame, text="Time")
        time_label.grid(row=5, column=1)
        self.time_val = Label(self.frame, text="")
        self.time_val.grid(row=5, column=2)
        time_units = Label(self.frame, text="UTC")
        time_units.grid(row=5, column=3)

        lat_label = Label(self.frame, text="Latitude")
        lat_label.grid(row=6, column=1)
        self.lat_val = Label(self.frame, text="")
        self.lat_val.grid(row=6, column=2)

        lon_label = Label(self.frame, text="Longitude")
        lon_label.grid(row=7, column=1)
        self.lon_val = Label(self.frame, text="")
        self.lon_val.grid(row=7, column=2)

        altm_label = Label(self.frame, text="Altitude")
        altm_label.grid(row=8, column=1)
        self.altm_val = Label(self.frame, text="")
        self.altm_val.grid(row=8, column=2)
        altm_units = Label(self.frame, text="meters")
        altm_units.grid(row=8, column=3)

        altft_label = Label(self.frame, text="Altitude")
        altft_label.grid(row=9, column=1)
        self.altft_val = Label(self.frame, text="")
        self.altft_val.grid(row=9, column=2)
        altft_units = Label(self.frame, text="feet")
        altft_units.grid(row=9, column=3)

        temp1_label = Label(self.frame, text="Temperature 1")
        temp1_label.grid(row=10, column=1)
        self.temp1_val = Label(self.frame, text="")
        self.temp1_val.grid(row=10, column=2)
        temp1_units = Label(self.frame, text="Celsius")
        temp1_units.grid(row=10, column=3)

        temp2_label = Label(self.frame, text="Temperature 2")
        temp2_label.grid(row=11, column=1)
        self.temp2_val = Label(self.frame, text="")
        self.temp2_val.grid(row=11, column=2)
        temp2_units = Label(self.frame, text="Celsius")
        temp2_units.grid(row=11, column=3)

        tempp_label = Label(self.frame, text="Temperature P")
        tempp_label.grid(row=12, column=1)
        self.tempp_val = Label(self.frame, text="")
        self.tempp_val.grid(row=12, column=2)
        tempp_units = Label(self.frame, text="Celsius")
        tempp_units.grid(row=12, column=3)

        press_label = Label(self.frame, text="Pressure")
        press_label.grid(row=13, column=1)
        self.press_val = Label(self.frame, text="")
        self.press_val.grid(row=13, column=2)
        press_units = Label(self.frame, text="milli Bar")
        press_units.grid(row=13, column=3)

        x_label = Label(self.frame, text="X")
        x_label.grid(row=14, column=1)
        self.x_val = Label(self.frame, text="")
        self.x_val.grid(row=14, column=2)
        x_units = Label(self.frame, text="milli g")
        x_units.grid(row=14, column=3)

        y_label = Label(self.frame, text="Y")
        y_label.grid(row=15, column=1)
        self.y_val = Label(self.frame, text="")
        self.y_val.grid(row=15, column=2)
        y_units = Label(self.frame, text="milli g")
        y_units.grid(row=15, column=3)

        z_label = Label(self.frame, text="Z")
        z_label.grid(row=16, column=1)
        self.z_val = Label(self.frame, text="")
        self.z_val.grid(row=16, column=2)
        z_units = Label(self.frame, text="milli g")
        z_units.grid(row=16, column=3)

        pack_s_label = Label(self.frame, text="Packets Sent")
        pack_s_label.grid(row=17, column=1)
        self.pack_s_val = Label(self.frame, text="")
        self.pack_s_val.grid(row=17, column=2)

        pack_r_label = Label(self.frame, text="Packets Received")
        pack_r_label.grid(row=18, column=1)
        self.pack_r_val = Label(self.frame, text="")
        self.pack_r_val.grid(row=18, column=2)

        pack_l_label = Label(self.frame, text="Packets Lost")
        pack_l_label.grid(row=19, column=1)
        self.pack_l_val = Label(self.frame, text="")
        self.pack_l_val.grid(row=19, column=2)

    def connect_board(self):
        if not self.board_connected and self.com_list.get() != "":
            self.board = serial.Serial(port=self.com_list.get(), baudrate=9600, timeout=.1)
            char = self.board.read().decode("utf-8")
            string_rec = char
            while char != '|':
                char = self.board.read().decode("utf-8")
                if char != '|' or '':
                    string_rec = string_rec + char
            self.board_val["text"] = string_rec
            self.board_connected = True
            print("Board Connected to " + str(self.com_list.get()))
        elif self.board_connected:
            print("Board Already Connected")
        else:
            print("Failed to Connect Board")
        return

    def connect_board2(self):
        if not self.board_connected2 and self.com_list2.get() != "":
            self.board2 = serial.Serial(port=self.com_list2.get(), baudrate=9600, timeout=.1)
            char = self.board2.read().decode("utf-8")
            string_rec = char
            while char != '|':
                char = self.board2.read().decode("utf-8")
                if char != '|' or '':
                    string_rec = string_rec + char
            self.board_val2["text"] = string_rec
            self.board_connected2 = True
            print("Board 2 Connected to " + str(self.com_list2.get()))
        elif self.board_connected2:
            print("Board 2 Already Connected")
        else:
            print("Failed to Connect Board 2")
        return

    def add_board(self):
        self.two_board_mode = True
        self.add_button.destroy()
        com_list_label2 = Label(self.frame, text="Board Port")
        com_list_label2.grid(row=0, column=4)
        self.com_list2 = ttk.Combobox(self.frame, values=self.portNames)
        self.com_list2.grid(row=0, column=5)
        com_select2 = Button(self.frame, text="Select", command=self.connect_board2)
        com_select2.grid(row=0, column=6)

        sel_i2c_label2 = Label(self.frame, text="I2C Addition")
        sel_i2c_label2.grid(row=1, column=4)
        self.sel_i2c_list2 = ttk.Combobox(self.frame, values=["None", "NEMO"])
        self.sel_i2c_list2.grid(row=1, column=5)
        sel_i2c_select2 = Button(self.frame, text="Select", command=self.connect_i2c2)
        sel_i2c_select2.grid(row=1, column=6)

        board_label2 = Label(self.frame, text="Board ID")
        board_label2.grid(row=4, column=4)
        self.board_val2 = Label(self.frame, text="")
        self.board_val2.grid(row=4, column=5)

        time_label2 = Label(self.frame, text="Time")
        time_label2.grid(row=5, column=4)
        self.time_val2 = Label(self.frame, text="")
        self.time_val2.grid(row=5, column=5)
        time_units2 = Label(self.frame, text="UTC")
        time_units2.grid(row=5, column=6)

        lat_label2 = Label(self.frame, text="Latitude")
        lat_label2.grid(row=6, column=4)
        self.lat_val2 = Label(self.frame, text="")
        self.lat_val2.grid(row=6, column=5)

        lon_label2 = Label(self.frame, text="Longitude")
        lon_label2.grid(row=7, column=4)
        self.lon_val2 = Label(self.frame, text="")
        self.lon_val2.grid(row=7, column=5)

        altm_label2 = Label(self.frame, text="Altitude")
        altm_label2.grid(row=8, column=4)
        self.altm_val2 = Label(self.frame, text="")
        self.altm_val2.grid(row=8, column=5)
        altm_units2 = Label(self.frame, text="meters")
        altm_units2.grid(row=8, column=6)

        altft_label2 = Label(self.frame, text="Altitude")
        altft_label2.grid(row=9, column=4)
        self.altft_val2 = Label(self.frame, text="")
        self.altft_val2.grid(row=9, column=5)
        altft_units2 = Label(self.frame, text="feet")
        altft_units2.grid(row=9, column=6)

        temp1_label2 = Label(self.frame, text="Temperature 1")
        temp1_label2.grid(row=10, column=4)
        self.temp1_val2 = Label(self.frame, text="")
        self.temp1_val2.grid(row=10, column=5)
        temp1_units2 = Label(self.frame, text="Celsius")
        temp1_units2.grid(row=10, column=6)

        temp2_label2 = Label(self.frame, text="Temperature 2")
        temp2_label2.grid(row=11, column=4)
        self.temp2_val2 = Label(self.frame, text="")
        self.temp2_val2.grid(row=11, column=5)
        temp2_units2 = Label(self.frame, text="Celsius")
        temp2_units2.grid(row=11, column=6)

        tempp_label2 = Label(self.frame, text="Temperature P")
        tempp_label2.grid(row=12, column=4)
        self.tempp_val2 = Label(self.frame, text="")
        self.tempp_val2.grid(row=12, column=5)
        tempp_units2 = Label(self.frame, text="Celsius")
        tempp_units2.grid(row=12, column=6)

        press_label2 = Label(self.frame, text="Pressure")
        press_label2.grid(row=13, column=4)
        self.press_val2 = Label(self.frame, text="")
        self.press_val2.grid(row=13, column=5)
        press_units2 = Label(self.frame, text="milli Bar")
        press_units2.grid(row=13, column=6)

        x_label2 = Label(self.frame, text="X")
        x_label2.grid(row=14, column=4)
        self.x_val2 = Label(self.frame, text="")
        self.x_val2.grid(row=14, column=5)
        x_units2 = Label(self.frame, text="milli g")
        x_units2.grid(row=14, column=6)

        y_label2 = Label(self.frame, text="Y")
        y_label2.grid(row=15, column=4)
        self.y_val2 = Label(self.frame, text="")
        self.y_val2.grid(row=15, column=5)
        y_units2 = Label(self.frame, text="milli g")
        y_units2.grid(row=15, column=6)

        z_label2 = Label(self.frame, text="Z")
        z_label2.grid(row=16, column=4)
        self.z_val2 = Label(self.frame, text="")
        self.z_val2.grid(row=16, column=5)
        z_units2 = Label(self.frame, text="milli g")
        z_units2.grid(row=16, column=6)

        pack_s_label2 = Label(self.frame, text="Packets Sent")
        pack_s_label2.grid(row=17, column=4)
        self.pack_s_val2 = Label(self.frame, text="")
        self.pack_s_val2.grid(row=17, column=5)

        pack_r_label2 = Label(self.frame, text="Packets Received")
        pack_r_label2.grid(row=18, column=4)
        self.pack_r_val2 = Label(self.frame, text="")
        self.pack_r_val2.grid(row=18, column=5)

        pack_l_label2 = Label(self.frame, text="Packets Lost")
        pack_l_label2.grid(row=19, column=4)
        self.pack_l_val2 = Label(self.frame, text="")
        self.pack_l_val2.grid(row=19, column=5)
        return

    def connect_i2c(self):
        if not self.i2c_connected and self.sel_i2c_list.get() != "":
            self.i2c_type = self.sel_i2c_list.get()
            if self.i2c_type == "None":
                print("No I2C Connected. No Additional Data.")
            elif self.i2c_type == "NEMO":
                print("I2C Connected to NEMO. Setting up Table")
                self.setup_nemo()
            self.i2c_connected = True
        elif self.i2c_connected:
            print("I2C Already Set Up")
        else:
            print("Please Select I2C Type")
        return

    def connect_i2c2(self):
        if not self.i2c_connected2 and self.sel_i2c_list2.get() != "":
            self.i2c_type2 = self.sel_i2c_list2.get()
            if self.i2c_type2 == "None":
                print("No I2C 2 Connected. No Additional Data.")
            elif self.i2c_type2 == "NEMO":
                print("I2C 2 Connected to NEMO. Setting up Table")
                self.setup_nemo2()
            self.i2c_connected2 = True
        elif self.i2c_connected2:
            print("I2C 2 Already Set Up")
        else:
            print("Please Select I2C 2 Type")
        return

    def setup_nemo(self):
        nemo_label = Label(self.frame, text="NEMO")
        nemo_label.grid(row=25, column=2)

        nemo_data_label = Label(self.frame, text="Data 1 Count")
        nemo_data_label.grid(row=26, column=1)
        self.nemo_data_val = Label(self.frame, text="")
        self.nemo_data_val.grid(row=26, column=2)

        nemo_hist_label = Label(self.frame, text="Data 2 Count")
        nemo_hist_label.grid(row=27, column=1)
        self.nemo_hist_val = Label(self.frame, text="")
        self.nemo_hist_val.grid(row=27,column=2)
        return

    def setup_nemo2(self):
        nemo_label = Label(self.frame, text="NEMO")
        nemo_label.grid(row=25, column=5)

        nemo_data_label2 = Label(self.frame, text="Data 1 Count")
        nemo_data_label2.grid(row=26, column=4)
        self.nemo_data_val2 = Label(self.frame, text="")
        self.nemo_data_val2.grid(row=26, column=5)

        nemo_hist_label2 = Label(self.frame, text="Data 2 Count")
        nemo_hist_label2.grid(row=27, column=4)
        self.nemo_hist_val2 = Label(self.frame, text="")
        self.nemo_hist_val2.grid(row=27, column=5)
        return

    def ready_check(self):
        if self.two_board_mode:
            if not self.board_connected:
                print("Board Not Connected")
            if not self.i2c_connected:
                print("I2C System Not Selected")
            if not self.board_connected2:
                print("Board 2 Not Connected")
            if not self.i2c_connected2:
                print("I2C System 2 Not Selected")
            if self.board_connected and self.i2c_connected and self.board_connected2 and self.i2c_connected2:
                print("System Starting")
                self.running = True
                self.running2 = True
                self.stop_select["state"] = NORMAL
                self.start_select["state"] = DISABLED
                self.run_b1_thread = threading.Thread(target=Board1Thread)
                self.run_b1_thread2 = threading.Thread(target=Board2Thread)
                self.run_b1_thread.start()
                self.run_b1_thread2.start()
        if not self.two_board_mode:
            if not self.board_connected:
                print("Board Not Connected")
            if not self.i2c_connected:
                print("I2C System Not Selected")
            if self.board_connected and self.i2c_connected:
                print("System Starting")
                self.running = True
                self.stop_select["state"] = NORMAL
                self.start_select["state"] = DISABLED
                self.run_b1_thread = threading.Thread(target=Board1Thread)
                self.run_b1_thread.start()
        return

    def sys_stop(self):
        if self.two_board_mode:
            print("Stopping System")
            self.running = False
            self.running2 = False
            self.stop_select["state"] = DISABLED
            self.start_select["state"] = NORMAL
        else:
            print("Stopping System")
            self.running = False
            self.stop_select["state"] = DISABLED
            self.start_select["state"] = NORMAL
        return


class Board1Thread(object):
    def __init__(self):
        self.data_output = np.zeros(500)
        self.board = ui.board
        self.data_stream = ""
        # print("Board1Thread INIT")
        self.sensor_data = np.zeros(500)
        self.nemo_data = np.zeros(500)
        self.nemo_hist = np.zeros(500)
        self.payload_gps = np.zeros(500)
        self.found_gga = False

        now = datetime.now()
        timedate = now.strftime("%Y%m%d_%H%M%S")
        cwd = os.getcwd()
        out = open(cwd + "\\outputfiles\\" + timedate + ".csv", "w", newline='')
        self.csvwriter = csv.writer(out)
        self.pack1cnt = 0
        self.pack2cnt = 0
        self.system_running()

    def system_running(self):
        while ui.running:
            test = 0
            while True:
                try:
                    test = self.board.read().decode("utf-8")
                    if test == '[':
                        break
                    if test == '{':
                        break
                    if test == '(':
                        break
                except:
                    print("IM STUCK")
                    pass

            if test == '[':
                char = self.board.read().decode("utf-8")
                string_rec = char
                while char != ']':
                    char = self.board.read().decode("utf-8")
                    if char != ']' or '':
                        string_rec = string_rec + char
                print("BOARD 1:" + string_rec)
                self.data_output = np.asarray(string_rec.split(','))
                rssi_snr = self.data_output[-2:]
                self.data_output = self.data_output[:-2].astype(int)
                payload_sensors = self.data_output[1:21].astype(int)

                payload_sensors[14] = 0
                self.payload_gps = np.asarray(("".join([chr(item) for item in self.data_output[22:-2]])).split(','), str)

                self.sensor_data[0] = (payload_sensors[0] << 8) + payload_sensors[1]
                self.sensor_data[1] = (payload_sensors[2] << 8) + payload_sensors[3]
                self.sensor_data[2] = (payload_sensors[4] << 8) + payload_sensors[5]
                self.sensor_data[3] = (payload_sensors[6] << 8) + payload_sensors[7]
                self.sensor_data[4] = (payload_sensors[8] << 8) + payload_sensors[9]
                self.sensor_data[5] = (payload_sensors[10] << 24) + (payload_sensors[11] << 16) + (payload_sensors[12] << 8) + payload_sensors[13]
                self.sensor_data[10] = (payload_sensors[14] << 24) + (payload_sensors[15] << 16) + (payload_sensors[16] << 8) + payload_sensors[17]
                self.sensor_data[11] = (payload_sensors[18] << 8) + payload_sensors[19]
                self.sensor_data[12] = self.sensor_data[12] + 1

                if self.sensor_data[0].astype(int) >> 15:
                    temp_list = list(bin(self.sensor_data[0].astype(int)))  # this is needed to do binary 2s complement
                    for j in range(len(temp_list) - 2):
                        # Flip bits
                        if temp_list[j + 2] == '1':
                            temp_list[j + 2] = '0'
                        else:
                            temp_list[j + 2] = '1'
                    temp_list = "".join(temp_list)  # join the list back together
                    self.sensor_data[0] = ~ int(temp_list, 2)  # convert the temp list back to a number
                if self.sensor_data[1].astype(int) >> 15:
                    temp_list = list(bin(self.sensor_data[1].astype(int)))  # this is needed to do binary 2s complement
                    for j in range(len(temp_list) - 2):
                        # Flip bits
                        if temp_list[j + 2] == '1':
                            temp_list[j + 2] = '0'
                        else:
                            temp_list[j + 2] = '1'
                    temp_list = "".join(temp_list)  # join the list back together
                    self.sensor_data[1] = ~ int(temp_list, 2)  # convert the temp list back to a number
                if self.sensor_data[10].astype(int) >> 15:
                    temp_list = list(bin(self.sensor_data[10].astype(int)))  # this is needed to do binary 2s complement
                    for j in range(len(temp_list) - 2):
                        # Flip bits
                        if temp_list[j + 2] == '1':
                            temp_list[j + 2] = '0'
                        else:
                            temp_list[j + 2] = '1'
                    temp_list = "".join(temp_list)  # join the list back together
                    self.sensor_data[10] = ~ int(temp_list, 2)  # convert the temp list back to a number
                self.sensor_data[0] = self.sensor_data[0] / (2 ** 7)  # convert temperature 1
                self.sensor_data[1] = self.sensor_data[1] / (2 ** 7)  # convert temperature 2
                self.sensor_data[2] = self.sensor_data[2] * 0.061  # convert accelerometer x
                self.sensor_data[3] = self.sensor_data[3] * 0.061  # convert accelerometer y
                self.sensor_data[4] = self.sensor_data[4] * 0.061  # convert accelerometer z
                self.sensor_data[5] = self.sensor_data[5]/100 # convert pressure
                self.sensor_data[10] = self.sensor_data[10]/100 # convert temperature P

                #  FIXME: GPS Parse is failing, figure out why
                gga_ind = np.where(self.payload_gps == "$GNGGA")  # find the index of GNGGA
                if len(gga_ind[0]) != 0:
                    # print("GGA: " + gga_ind.astype(str))
                    try:
                        self.sensor_data[6] = (self.payload_gps[gga_ind[0][0] + 1].astype(float)).astype(np.int64)
                        self.found_gga = True
                    except ValueError:
                        self.found_gga = False
                else:  # if we don't get this string, do some searching to try to get it another way
                    for i in range(len(self.payload_gps)):
                        if "$GNGGA" in self.payload_gps[i]:
                            # print("STR: " + payload_gps[i])
                            if i != len(self.payload_gps) - 1:
                                try:
                                    self.sensor_data[6] = (self.payload_gps[i + 1].astype(float)).astype(np.int64)
                                    self.found_gga = True
                                    # print("alt GGA: " + str(gga_ind))
                                    break
                                except ValueError:
                                    pass
                if self.found_gga:
                    self.found_gga = False
                else:
                    self.sensor_data[6] = 0

                NS_ind = np.where(self.payload_gps == "N")
                if len(NS_ind[0]) != 0:
                    if NS_ind[0][0] != 0:
                        for i in range(len(NS_ind[0])):
                            try:
                                self.sensor_data[7] = (self.payload_gps[NS_ind[0][i] - 1].astype(float)) / 100
                                temp_dec = self.sensor_data[7] % 1
                                self.sensor_data[7] -= temp_dec
                                temp_dec = (temp_dec * 100) / 60
                                self.sensor_data[7] += temp_dec
                            except ValueError:
                                if i == len(NS_ind[0]) - 1:
                                    self.sensor_data[7] = 0
                                pass
                    else:
                        self.sensor_data[7] = 0
                else:
                    NS_ind = np.where(self.payload_gps == "S")
                    if len(NS_ind[0]) != 0:
                        if NS_ind[0][0] != 0:
                            for i in range(len(NS_ind[0])):
                                try:
                                    # set negative if in S hemisphere
                                    self.sensor_data[7] = (self.payload_gps[NS_ind[0][i] - 1].astype(float)) / 100
                                    temp_dec = self.sensor_data[7] % 1
                                    self.sensor_data[7] -= temp_dec
                                    temp_dec = (temp_dec * 100) / 60
                                    self.sensor_data[7] += temp_dec
                                    self.sensor_data[7] = self.sensor_data[7] * -1
                                except ValueError:
                                    if i == len(NS_ind[0]) - 1:
                                        self.sensor_data[7] = 0
                                    pass
                        else:
                            self.sensor_data[7] = 0
                    else:
                        self.sensor_data[7] = 0

                # ARRAY TABLE #
                # 6 = time | 7 = GPS coords N/S | 8 = GPS coords E/W | 9 = height in m
                EW_ind = np.where(self.payload_gps == "E")
                if len(EW_ind[0]) != 0:
                    if EW_ind[0][0] != 0:
                        for i in range(len(EW_ind[0])):
                            try:
                                self.sensor_data[8] = (self.payload_gps[EW_ind[0][i] - 1].astype(float)) / 100
                                temp_dec = self.sensor_data[8] % 1
                                self.sensor_data[8] -= temp_dec
                                temp_dec = (temp_dec * 100) / 60
                                self.sensor_data[8] += temp_dec
                            except ValueError:
                                if i == len(EW_ind[0]) - 1:
                                    self.sensor_data[8] = 0
                                pass
                    else:
                        self.sensor_data[8] = 0
                else:
                    EW_ind = np.where(self.payload_gps == "W")
                    if len(EW_ind[0]) != 0:
                        if EW_ind[0][0] != 0:
                            for i in range(len(EW_ind[0])):
                                try:
                                    # set negative if in S hemisphere
                                    self.sensor_data[8] = (self.payload_gps[EW_ind[0][i] - 1].astype(float)) / 100
                                    temp_dec = self.sensor_data[8] % 1
                                    self.sensor_data[8] -= temp_dec
                                    temp_dec = (temp_dec * 100) / 60
                                    self.sensor_data[8] += temp_dec
                                    self.sensor_data[8] = self.sensor_data[8] * -1
                                except ValueError:
                                    if i == len(EW_ind[0]) - 1:
                                        self.sensor_data[8] = 0
                                    pass
                        else:
                            self.sensor_data[8] = 0
                    else:
                        self.sensor_data[8] = 0

                M_ind = np.where(self.payload_gps == "M")
                if len(M_ind[0]) != 0:
                    if M_ind[0][0] != 0:
                        try:
                            height_M = (self.payload_gps[M_ind[0][0] - 1].astype(float)).astype(np.int64)
                        except ValueError:
                            height_M = self.sensor_data[9]
                        if height_M < 0:
                            try:
                                height_M = (self.payload_gps[M_ind[0][1] - 1].astype(float)).astype(np.int64)
                            except ValueError:
                                height_M = self.sensor_data[9]
                            if height_M < 0:
                                height_M = 0
                    else:
                        height_M = 0
                else:
                    height_M = 0
                self.sensor_data[9] = height_M

                time = list((self.sensor_data[6].astype(int)).astype(str))
                if len(time) == 5:
                    time.insert(0, '0')
                elif len(time) == 4:
                    time.insert(0, '0')
                    time.insert(0, '0')
                try:
                    ui.time_val["text"] = time[0] + time[1] + ":" + time[2] + time[3] + ":" + time[4] + time[5]
                except IndexError:
                    ui.time_val["text"] = "00:00:00"
                ui.lat_val["text"] = str(self.sensor_data[7])
                ui.lon_val["text"] = str(self.sensor_data[8])
                ui.altm_val["text"] = str(self.sensor_data[9])
                ui.altft_val["text"] = str((self.sensor_data[9].astype(int)*3.28084))
                ui.temp1_val["text"] = str(self.sensor_data[0])
                ui.temp2_val["text"] = str(self.sensor_data[1])
                ui.tempp_val["text"] = str(self.sensor_data[10])
                ui.press_val["text"] = str(self.sensor_data[5])
                ui.x_val["text"] = str(self.sensor_data[2])
                ui.y_val["text"] = str(self.sensor_data[3])
                ui.z_val["text"] = str(self.sensor_data[4])
                ui.pack_s_val["text"] = str(self.sensor_data[11])
                ui.pack_r_val["text"] = str(self.sensor_data[12])
                ui.pack_l_val["text"] = str(self.sensor_data[11] - self.sensor_data[12])
                self.csvwriter.writerow(self.data_output)
            elif test == '{':
                char = self.board.read().decode("utf-8")
                string_rec = char
                while char != '}':
                    char = self.board.read().decode("utf-8")
                    if char != '}' or '':
                        string_rec = string_rec + char
                print("BOARD1:" + string_rec)
                self.pack1cnt = self.pack1cnt + 1
                ui.nemo_data_val["text"] = self.pack1cnt
                self.data_output = np.asarray(string_rec.split(','))
                self.csvwriter.writerow(self.data_output)
            elif test == '(':
                char = self.board.read().decode("utf-8")
                string_rec = char
                while char != ')':
                    char = self.board.read().decode("utf-8")
                    if char != ')' or '':
                        string_rec = string_rec + char
                print("BOARD 1:" + string_rec)
                self.pack2cnt = self.pack2cnt + 1
                ui.nemo_hist_val["text"] = self.pack2cnt
                self.data_output = np.asarray(string_rec.split(','))
                self.csvwriter.writerow(self.data_output)
            else:
                print("TEST FAILED")

        return


class Board2Thread(object):
    def __init__(self):
        self.data_output = np.zeros(500)
        self.board = ui.board2
        self.data_stream = ""
        # print("Board1Thread INIT")
        self.sensor_data = np.zeros(500)
        self.nemo_data = np.zeros(500)
        self.nemo_hist = np.zeros(500)
        self.payload_gps = np.zeros(500)
        self.found_gga = False

        now = datetime.now()
        timedate = now.strftime("%Y%m%d_%H%M%S")
        cwd = os.getcwd()
        out = open(cwd + "\\outputfiles2\\" + timedate + ".csv", "w", newline='')
        self.csvwriter = csv.writer(out)
        self.system_running()

    def system_running(self):
        pack1cnt = 0
        pack2cnt = 0
        while ui.running2:
            # self.data_stream = self.board.read()
            test = 0
            while True:
                try:
                    #     # Peels of leading char
                    #     try:
                    #         test = self.board.read().decode("utf-8")
                    #         # if test == '[':
                    #         #     print("YES")
                    #         #     start_flag = True
                    #     except:
                    #         pass
                    # print("couldn't decode character (this is okay)")  # This line can be used for debug if desired
                    test = self.board.read().decode("utf-8")
                    # print(test)
                    if test == '[':
                        break
                    if test == '{':
                        break
                    if test == '(':
                        break
                except:
                    print("IM STUCK")
                    pass

            if test == '[':
                char = self.board.read().decode("utf-8")
                string_rec = char
                while char != ']':
                    char = self.board.read().decode("utf-8")
                    if char != ']' or '':
                        string_rec = string_rec + char
                print("BOARD 2:" + string_rec)
                self.data_output = np.asarray(string_rec.split(','))
                rssi_snr = self.data_output[-2:]
                self.data_output = self.data_output[:-2].astype(int)
                payload_sensors = self.data_output[1:21].astype(int)

                payload_sensors[14] = 0
                self.payload_gps = np.asarray(("".join([chr(item) for item in self.data_output[22:-2]])).split(','),
                                              str)

                self.sensor_data[0] = (payload_sensors[0] << 8) + payload_sensors[1]
                self.sensor_data[1] = (payload_sensors[2] << 8) + payload_sensors[3]
                self.sensor_data[2] = (payload_sensors[4] << 8) + payload_sensors[5]
                self.sensor_data[3] = (payload_sensors[6] << 8) + payload_sensors[7]
                self.sensor_data[4] = (payload_sensors[8] << 8) + payload_sensors[9]
                self.sensor_data[5] = (payload_sensors[10] << 24) + (payload_sensors[11] << 16) + (
                            payload_sensors[12] << 8) + payload_sensors[13]
                self.sensor_data[10] = (payload_sensors[14] << 24) + (payload_sensors[15] << 16) + (
                            payload_sensors[16] << 8) + payload_sensors[17]
                self.sensor_data[11] = (payload_sensors[18] << 8) + payload_sensors[19]
                self.sensor_data[12] = self.sensor_data[12] + 1

                if self.sensor_data[0].astype(int) >> 15:
                    temp_list = list(bin(self.sensor_data[0].astype(int)))  # this is needed to do binary 2s complement
                    for j in range(len(temp_list) - 2):
                        # Flip bits
                        if temp_list[j + 2] == '1':
                            temp_list[j + 2] = '0'
                        else:
                            temp_list[j + 2] = '1'
                    temp_list = "".join(temp_list)  # join the list back together
                    self.sensor_data[0] = ~ int(temp_list, 2)  # convert the temp list back to a number
                if self.sensor_data[1].astype(int) >> 15:
                    temp_list = list(bin(self.sensor_data[1].astype(int)))  # this is needed to do binary 2s complement
                    for j in range(len(temp_list) - 2):
                        # Flip bits
                        if temp_list[j + 2] == '1':
                            temp_list[j + 2] = '0'
                        else:
                            temp_list[j + 2] = '1'
                    temp_list = "".join(temp_list)  # join the list back together
                    self.sensor_data[1] = ~ int(temp_list, 2)  # convert the temp list back to a number
                if self.sensor_data[10].astype(int) >> 15:
                    temp_list = list(bin(self.sensor_data[10].astype(int)))  # this is needed to do binary 2s complement
                    for j in range(len(temp_list) - 2):
                        # Flip bits
                        if temp_list[j + 2] == '1':
                            temp_list[j + 2] = '0'
                        else:
                            temp_list[j + 2] = '1'
                    temp_list = "".join(temp_list)  # join the list back together
                    self.sensor_data[10] = ~ int(temp_list, 2)  # convert the temp list back to a number
                self.sensor_data[0] = self.sensor_data[0] / (2 ** 7)  # convert temperature 1
                self.sensor_data[1] = self.sensor_data[1] / (2 ** 7)  # convert temperature 2
                self.sensor_data[2] = self.sensor_data[2] * 0.061  # convert accelerometer x
                self.sensor_data[3] = self.sensor_data[3] * 0.061  # convert accelerometer y
                self.sensor_data[4] = self.sensor_data[4] * 0.061  # convert accelerometer z
                self.sensor_data[5] = self.sensor_data[5] / 100  # convert pressure
                self.sensor_data[10] = self.sensor_data[10] / 100  # convert temperature P

                gga_ind = np.where(self.payload_gps == "$GNGGA")  # find the index of GNGGA
                if len(gga_ind[0]) != 0:
                    # print("GGA: " + gga_ind.astype(str))
                    try:
                        self.sensor_data[6] = (self.payload_gps[gga_ind[0][0] + 1].astype(float)).astype(np.int64)
                        self.found_gga = True
                    except ValueError:
                        self.found_gga = False
                else:  # if we don't get this string, do some searching to try to get it another way
                    for i in range(len(self.payload_gps)):
                        if "$GNGGA" in self.payload_gps[i]:
                            # print("STR: " + payload_gps[i])
                            if i != len(self.payload_gps) - 1:
                                try:
                                    self.sensor_data[6] = (self.payload_gps[i + 1].astype(float)).astype(np.int64)
                                    self.found_gga = True
                                    # print("alt GGA: " + str(gga_ind))
                                    break
                                except ValueError:
                                    pass
                if self.found_gga:
                    self.found_gga = False
                else:
                    self.sensor_data[6] = 0

                NS_ind = np.where(self.payload_gps == "N")
                if len(NS_ind[0]) != 0:
                    if NS_ind[0][0] != 0:
                        for i in range(len(NS_ind[0])):
                            try:
                                self.sensor_data[7] = (self.payload_gps[NS_ind[0][i] - 1].astype(float)) / 100
                                temp_dec = self.sensor_data[7] % 1
                                self.sensor_data[7] -= temp_dec
                                temp_dec = (temp_dec * 100) / 60
                                self.sensor_data[7] += temp_dec
                            except ValueError:
                                if i == len(NS_ind[0]) - 1:
                                    self.sensor_data[7] = 0
                                pass
                    else:
                        self.sensor_data[7] = 0
                else:
                    NS_ind = np.where(self.payload_gps == "S")
                    if len(NS_ind[0]) != 0:
                        if NS_ind[0][0] != 0:
                            for i in range(len(NS_ind[0])):
                                try:
                                    # set negative if in S hemisphere
                                    self.sensor_data[7] = (self.payload_gps[NS_ind[0][i] - 1].astype(float)) / 100
                                    temp_dec = self.sensor_data[7] % 1
                                    self.sensor_data[7] -= temp_dec
                                    temp_dec = (temp_dec * 100) / 60
                                    self.sensor_data[7] += temp_dec
                                    self.sensor_data[7] = self.sensor_data[7] * -1
                                except ValueError:
                                    if i == len(NS_ind[0]) - 1:
                                        self.sensor_data[7] = 0
                                    pass
                        else:
                            self.sensor_data[7] = 0
                    else:
                        self.sensor_data[7] = 0

                # ARRAY TABLE #
                # 6 = time | 7 = GPS coords N/S | 8 = GPS coords E/W | 9 = height in m
                EW_ind = np.where(self.payload_gps == "E")
                if len(EW_ind[0]) != 0:
                    if EW_ind[0][0] != 0:
                        for i in range(len(EW_ind[0])):
                            try:
                                self.sensor_data[8] = (self.payload_gps[EW_ind[0][i] - 1].astype(float)) / 100
                                temp_dec = self.sensor_data[8] % 1
                                self.sensor_data[8] -= temp_dec
                                temp_dec = (temp_dec * 100) / 60
                                self.sensor_data[8] += temp_dec
                            except ValueError:
                                if i == len(EW_ind[0]) - 1:
                                    self.sensor_data[8] = 0
                                pass
                    else:
                        self.sensor_data[8] = 0
                else:
                    EW_ind = np.where(self.payload_gps == "W")
                    if len(EW_ind[0]) != 0:
                        if EW_ind[0][0] != 0:
                            for i in range(len(EW_ind[0])):
                                try:
                                    # set negative if in S hemisphere
                                    self.sensor_data[8] = (self.payload_gps[EW_ind[0][i] - 1].astype(float)) / 100
                                    temp_dec = self.sensor_data[8] % 1
                                    self.sensor_data[8] -= temp_dec
                                    temp_dec = (temp_dec * 100) / 60
                                    self.sensor_data[8] += temp_dec
                                    self.sensor_data[8] = self.sensor_data[8] * -1
                                except ValueError:
                                    if i == len(EW_ind[0]) - 1:
                                        self.sensor_data[8] = 0
                                    pass
                        else:
                            self.sensor_data[8] = 0
                    else:
                        self.sensor_data[8] = 0

                M_ind = np.where(self.payload_gps == "M")
                if len(M_ind[0]) != 0:
                    if M_ind[0][0] != 0:
                        try:
                            height_M = (self.payload_gps[M_ind[0][0] - 1].astype(float)).astype(np.int64)
                        except ValueError:
                            height_M = self.sensor_data[9]
                        if height_M < 0:
                            try:
                                height_M = (self.payload_gps[M_ind[0][1] - 1].astype(float)).astype(np.int64)
                            except ValueError:
                                height_M = self.sensor_data[9]
                            if height_M < 0:
                                height_M = 0
                    else:
                        height_M = 0
                else:
                    height_M = 0
                self.sensor_data[9] = height_M

                time = list((self.sensor_data[6].astype(int)).astype(str))
                if len(time) == 5:
                    time.insert(0, '0')
                elif len(time) == 4:
                    time.insert(0, '0')
                    time.insert(0, '0')
                try:
                    ui.time_val2["text"] = time[0] + time[1] + ":" + time[2] + time[3] + ":" + time[4] + time[5]
                except IndexError:
                    ui.time_val2["text"] = "00:00:00"
                ui.lat_val2["text"] = str(self.sensor_data[7])
                ui.lon_val2["text"] = str(self.sensor_data[8])
                ui.altm_val2["text"] = str(self.sensor_data[9])
                ui.altft_val2["text"] = str((self.sensor_data[9].astype(int) * 3.28084))
                ui.temp1_val2["text"] = str(self.sensor_data[0])
                ui.temp2_val2["text"] = str(self.sensor_data[1])
                ui.tempp_val2["text"] = str(self.sensor_data[10])
                ui.press_val2["text"] = str(self.sensor_data[5])
                ui.x_val2["text"] = str(self.sensor_data[2])
                ui.y_val2["text"] = str(self.sensor_data[3])
                ui.z_val2["text"] = str(self.sensor_data[4])
                ui.pack_s_val2["text"] = str(self.sensor_data[11])
                ui.pack_r_val2["text"] = str(self.sensor_data[12])
                ui.pack_l_val2["text"] = str(self.sensor_data[11] - self.sensor_data[12])
                self.csvwriter.writerow(self.data_output)
            elif test == '{':
                char = self.board.read().decode("utf-8")
                string_rec = char
                while char != '}':
                    char = self.board.read().decode("utf-8")
                    if char != '}' or '':
                        string_rec = string_rec + char
                print("BOARD 2:" + string_rec)
                pack1cnt = pack1cnt + 1
                ui.nemo_data_val2["text"] = pack1cnt
                self.data_output = np.asarray(string_rec.split(','))
                self.csvwriter.writerow(self.data_output)
            elif test == '(':
                char = self.board.read().decode("utf-8")
                string_rec = char
                while char != ')':
                    char = self.board.read().decode("utf-8")
                    if char != ')' or '':
                        string_rec = string_rec + char
                print("BOARD 2:" + string_rec)
                pack2cnt = pack2cnt + 1
                ui.nemo_hist_val2["text"] = pack2cnt
                self.data_output = np.asarray(string_rec.split(','))
                self.csvwriter.writerow(self.data_output)
            else:
                print("TEST FAILED")
        return


if __name__ == "__main__":
    main_window = tk.Tk()
    ui = Window()
    ui.setup_ui(main_window)
    main_window.mainloop()
