import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import *
from tkinter import ttk
import threading
import numpy as np

import parse
from parse import Parse
import sys

#  TODO: Fix Parsing
#  TODO: Test New Thread Call
#  TODO: Add NEMO Output

from lora_serial import SerialConn


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
            self.board = SerialConn(self.com_list.get(), 9600)
            self.board_connected = True
            print("Board Connected to " + str(self.com_list.get()))
        elif self.board_connected:
            print("Board Already Connected")
        else:
            print("Failed to Connect Board")
        return

    def connect_board2(self):
        if not self.board_connected2 and self.com_list2.get() != "":
            self.board2 = SerialConn(self.com_list2.get(), 9600)
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
        return

    def setup_nemo2(self):
        nemo_label = Label(self.frame, text="NEMO")
        nemo_label.grid(row=25, column=5)
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
                self.thread1 = parse.Parse(main_window)
                self.run_b1_thread = threading.Thread(target=self.thread1)
                self.thread2 = parse.Parse(main_window)
                self.run_b1_thread2 = threading.Thread(target=self.thread2)
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
                self.thread1 = parse.Parse(main_window)
                self.run_b1_thread = threading.Thread(target=self.thread1)
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


# class Board1Thread(object):
#     def __init__(self):
#         self.data_output = np.zeros(500)
#         self.board = ui.board
#         self.data_stream = ""
#         # print("Board1Thread INIT")
#         self.sensor_data = np.zeros(500)
#         self.payload_gps = np.zeros(500)
#         self.found_gga = False
#         self.system_running()
#
#     def system_running(self):
#         while ui.running:
#             self.data_stream = self.board.rec_data()
#             test = 0
#             while test != '[':
#                 try:
#                     test = self.board.rec_data().decode("utf-8")
#                     # if test == '[':
#                     #     print("YES")
#                     #     start_flag = True
#                 except:
#                     pass
#                     # print("couldn't decode character (this is okay)")  # This line can be used for debug if desired
#
#             char = self.board.rec_data().decode("utf-8")
#             string_rec = char
#             while char != ']':
#                 char = self.board.rec_data().decode("utf-8")
#                 if char != ']' or '':
#                     string_rec = string_rec + char
#                 # print(string_rec)
#             self.data_output = np.asarray(string_rec.split(','))
#             # print(self.data_output)
#
#             # rssi_snr = self.data_output[-2:]
#             # self.data_output = self.data_output[-2:].astype(int)
#
#             self.sensor_data[0] = (self.data_output[1].astype(int) << 8) + self.data_output[2].astype(int)  # set internal temp
#             self.sensor_data[1] = (self.data_output[3].astype(int) << 8) + self.data_output[4].astype(int)   # set external temp
#             self.sensor_data[2] = (self.data_output[5].astype(int)  << 8) + self.data_output[6].astype(int)   # set accel x
#             self.sensor_data[3] = (self.data_output[7].astype(int)  << 8) + self.data_output[8].astype(int)   # set accel y
#             self.sensor_data[4] = (self.data_output[9].astype(int)  << 8) + self.data_output[10].astype(int)   # set accel z
#             self.sensor_data[5] = (self.data_output[11].astype(int)  << 24) + (self.data_output[12].astype(int)  << 16) + (self.data_output[13].astype(int)  << 8) + \
#                              self.data_output[14].astype(int)
#             self.sensor_data[10] = (self.data_output[15].astype(int)  << 24) + (self.data_output[16].astype(int)  << 16) + (self.data_output[17].astype(int)  << 8) + \
#                               self.data_output[18].astype(int)
#             self.sensor_data[11] = (self.data_output[19].astype(int)  << 8) + self.data_output[20].astype(int)
#
#             if self.sensor_data[0].astype(int) >> 15:
#                 temp_list = list(bin(self.sensor_data[0].astype(int)))
#                 for j in range(len(temp_list)-2):
#                     if temp_list[j+2] == '1':
#                         temp_list[j+2] = '0'
#                     else:
#                         temp_list[j+2] = '1'
#                 temp_list = "".join(temp_list)
#                 self.sensor_data[0] = ~ int(temp_list, 2)
#                 self.sensor_data[0] = self.sensor_data[0] / (2**7)
#
#             if self.sensor_data[1].astype(int) >> 15:
#                 temp_list = list(bin(self.sensor_data[1].astype(int)))
#                 for j in range(len(temp_list)-2):
#                     if temp_list[j+2] == '1':
#                         temp_list[j+2] = '0'
#                     else:
#                         temp_list[j+2] = '1'
#                 temp_list = "".join(temp_list)
#                 self.sensor_data[1] = ~ int(temp_list, 2)
#                 self.sensor_data[1] = self.sensor_data[1] / (2**7)
#
#             self.sensor_data[2] = self.sensor_data[2] * 0.061
#             self.sensor_data[3] = self.sensor_data[3] * 0.061
#             self.sensor_data[4] = self.sensor_data[4] * 0.061
#
#             self.sensor_data[5] = self.sensor_data[5]/100
#             self.sensor_data[10] = self.sensor_data[10]/100
#
#             placeholder = "" + str(self.data_output[22:-2])
#             self.payload_gps = np.asarray(placeholder.split(','), np.str_)
#
#             gga_ind = np.where(self.payload_gps == "$GNGGA")  # find the index of GNGGA
#             if len(gga_ind[0]) != 0:
#                 # print("GGA: " + gga_ind.astype(str))
#                 try:
#                     self.sensor_data[6] = (self.payload_gps[gga_ind[0][0] + 1].astype(np.float)).astype(np.int64)
#                     self.found_gga = True
#                 except ValueError:
#                     self.found_gga = False
#             else:  # if we don't get this string, do some searching to try to get it another way
#                 for i in range(len(self.payload_gps)):
#                     if "$GNGGA" in self.payload_gps[i]:
#                         # print("STR: " + payload_gps[i])
#                         if i != len(self.payload_gps) - 1:
#                             try:
#                                 self.sensor_data[6] = (self.payload_gps[i + 1].astype(np.float)).astype(np.int64)
#                                 self.found_gga = True
#                                 # print("alt GGA: " + str(gga_ind))
#                                 break
#                             except ValueError:
#                                 pass
#             if self.found_gga:
#                 self.found_gga = False
#             else:
#                 self.sensor_data[6] = 0
#
#             NS_ind = np.where(self.payload_gps == "N")
#             if len(NS_ind[0]) != 0:
#                 if NS_ind[0][0] != 0:
#                     for i in range(len(NS_ind[0])):
#                         try:
#                             self.sensor_data[7] = (self.payload_gps[NS_ind[0][i] - 1].astype(np.float)) / 100
#                             temp_dec = self.sensor_data[7] % 1
#                             self.sensor_data[7] -= temp_dec
#                             temp_dec = (temp_dec * 100) / 60
#                             self.sensor_data[7] += temp_dec
#                         except ValueError:
#                             if i == len(NS_ind[0]) - 1:
#                                 self.sensor_data[7] = 0
#                             pass
#                 else:
#                     self.sensor_data[7] = 0
#             else:
#                 NS_ind = np.where(self.payload_gps == "S")
#                 if len(NS_ind[0]) != 0:
#                     if NS_ind[0][0] != 0:
#                         for i in range(len(NS_ind[0])):
#                             try:
#                                 # set negative if in S hemisphere
#                                 self.sensor_data[7] = (self.payload_gps[NS_ind[0][i] - 1].astype(np.float)) / 100
#                                 temp_dec = self.sensor_data[7] % 1
#                                 self.sensor_data[7] -= temp_dec
#                                 temp_dec = (temp_dec * 100) / 60
#                                 self.sensor_data[7] += temp_dec
#                                 self.sensor_data[7] = self.sensor_data[7] * -1
#                             except ValueError:
#                                 if i == len(NS_ind[0]) - 1:
#                                     self.sensor_data[7] = 0
#                                 pass
#                     else:
#                         self.sensor_data[7] = 0
#                 else:
#                     self.sensor_data[7] = 0
#
#             # ARRAY TABLE #
#             # 6 = time | 7 = GPS coords N/S | 8 = GPS coords E/W | 9 = height in m
#             EW_ind = np.where(self.payload_gps == "E")
#             if len(EW_ind[0]) != 0:
#                 if EW_ind[0][0] != 0:
#                     for i in range(len(EW_ind[0])):
#                         try:
#                             self.sensor_data[8] = (self.payload_gps[EW_ind[0][i] - 1].astype(np.float)) / 100
#                             temp_dec = self.sensor_data[8] % 1
#                             self.sensor_data[8] -= temp_dec
#                             temp_dec = (temp_dec * 100) / 60
#                             self.sensor_data[8] += temp_dec
#                         except ValueError:
#                             if i == len(EW_ind[0]) - 1:
#                                 self.sensor_data[8] = 0
#                             pass
#                 else:
#                     self.sensor_data[8] = 0
#             else:
#                 EW_ind = np.where(self.payload_gps == "W")
#                 if len(EW_ind[0]) != 0:
#                     if EW_ind[0][0] != 0:
#                         for i in range(len(EW_ind[0])):
#                             try:
#                                 # set negative if in S hemisphere
#                                 self.sensor_data[8] = (self.payload_gps[EW_ind[0][i] - 1].astype(np.float)) / 100
#                                 temp_dec = self.sensor_data[8] % 1
#                                 self.sensor_data[8] -= temp_dec
#                                 temp_dec = (temp_dec * 100) / 60
#                                 self.sensor_data[8] += temp_dec
#                                 self.sensor_data[8] = self.sensor_data[8] * -1
#                             except ValueError:
#                                 if i == len(EW_ind[0]) - 1:
#                                     self.sensor_data[8] = 0
#                                 pass
#                     else:
#                         self.sensor_data[8] = 0
#                 else:
#                     self.sensor_data[8] = 0
#
#             M_ind = np.where(self.payload_gps == "M")
#             if len(M_ind[0]) != 0:
#                 if M_ind[0][0] != 0:
#                     try:
#                         height_M = (self.payload_gps[M_ind[0][0] - 1].astype(np.float)).astype(np.int64)
#                     except ValueError:
#                         height_M = self.sensor_data[9]
#                     if height_M < 0:
#                         try:
#                             height_M = (self.payload_gps[M_ind[0][1] - 1].astype(np.float)).astype(np.int64)
#                         except ValueError:
#                             height_M = self.sensor_data[9]
#                         if height_M < 0:
#                             height_M = 0
#                 else:
#                     height_M = 0
#             else:
#                 height_M = 0
#             self.sensor_data[9] = height_M
#
#             # print("Internal Temp:   " + str(self.sensor_data[0]))
#             # print("External Temp:   " + str(self.sensor_data[1]))
#             # print("X Accel:     " + str(self.sensor_data[2]))
#             # print("Y Accel:     " + str(self.sensor_data[3]))
#             # print("Z Accel:     " + str(self.sensor_data[4]))
#             # print("Pressure:    " + str(self.sensor_data[5]))
#             # print("Time: " + str(self.sensor_data[6]))
#             # print("Latitude:  " + str(self.sensor_data[7]))
#             # print("Longitude:  " + str(self.sensor_data[8]))
#             # print("Altitude:  "+ str(self.sensor_data[9]))
#             # print("Pressure Temp: " + str(self.sensor_data[10]))
#             # print("Packets sent: " + str(self.sensor_data[11]))
#             # print("Packets received " + str(self.sensor_data[12]))
#
#             ui.time_val["text"] = str(self.sensor_data[6])
#             ui.lat_val["text"] = str(self.sensor_data[7])
#             ui.lon_val["text"] = str(self.sensor_data[8])
#             ui.altm_val["text"] = str(self.sensor_data[9])
#             ui.altft_val["text"] = str((self.sensor_data[9].astype(int)*3.28084))
#             ui.temp1_val["text"] = str(self.sensor_data[0])
#             ui.temp2_val["text"] = str(self.sensor_data[1])
#             ui.tempp_val["text"] = str(self.sensor_data[10])
#             ui.press_val["text"] = str(self.sensor_data[5])
#             ui.x_val["text"] = str(self.sensor_data[2])
#             ui.y_val["text"] = str(self.sensor_data[3])
#             ui.z_val["text"] = str(self.sensor_data[4])
#
#
#         return

# class Board2Thread(object):
#     def __init__(self):
#         self.data_output = np.zeros(500)
#         self.board = ui.board2
#         self.data_stream = ""
#         # print("Board1Thread2 INIT")
#         self.sensor_data = np.zeros(500)
#         self.payload_gps = np.zeros(500)
#         self.found_gga = False
#         self.system_running()
#
#     def system_running(self):
#         while ui.running2:
#             self.data_stream = self.board.rec_data()
#             test = 0
#             while test != '[':
#                 try:
#                     test = self.board.rec_data().decode("utf-8")
#                     # if test == '[':
#                     #     print("YES")
#                     #     start_flag = True
#                 except:
#                     pass
#                     # print("couldn't decode character (this is okay)")  # This line can be used for debug if desired
#
#             char = self.board.rec_data().decode("utf-8")
#             string_rec = char
#             while char != ']':
#                 char = self.board.rec_data().decode("utf-8")
#                 if char != ']' or '':
#                     string_rec = string_rec + char
#                 # print(string_rec)
#             self.data_output = np.asarray(string_rec.split(','))
#             # print(self.data_output)
#
#             # rssi_snr = self.data_output[-2:]
#             # self.data_output = self.data_output[-2:].astype(int)
#
#             self.sensor_data[0] = (self.data_output[1].astype(int) << 8) + self.data_output[2].astype(
#                 int)  # set internal temp
#             self.sensor_data[1] = (self.data_output[3].astype(int) << 8) + self.data_output[4].astype(
#                 int)  # set external temp
#             self.sensor_data[2] = (self.data_output[5].astype(int) << 8) + self.data_output[6].astype(
#                 int)  # set accel x
#             self.sensor_data[3] = (self.data_output[7].astype(int) << 8) + self.data_output[8].astype(
#                 int)  # set accel y
#             self.sensor_data[4] = (self.data_output[9].astype(int) << 8) + self.data_output[10].astype(
#                 int)  # set accel z
#             self.sensor_data[5] = (self.data_output[11].astype(int) << 24) + (
#                         self.data_output[12].astype(int) << 16) + (self.data_output[13].astype(int) << 8) + \
#                                   self.data_output[14].astype(int)
#             self.sensor_data[10] = (self.data_output[15].astype(int) << 24) + (
#                         self.data_output[16].astype(int) << 16) + (self.data_output[17].astype(int) << 8) + \
#                                    self.data_output[18].astype(int)
#             self.sensor_data[11] = (self.data_output[19].astype(int) << 8) + self.data_output[20].astype(int)
#
#             if self.sensor_data[0].astype(int) >> 15:
#                 temp_list = list(bin(self.sensor_data[0].astype(int)))
#                 for j in range(len(temp_list) - 2):
#                     if temp_list[j + 2] == '1':
#                         temp_list[j + 2] = '0'
#                     else:
#                         temp_list[j + 2] = '1'
#                 temp_list = "".join(temp_list)
#                 self.sensor_data[0] = ~ int(temp_list, 2)
#                 self.sensor_data[0] = self.sensor_data[0] / (2 ** 7)
#
#             if self.sensor_data[1].astype(int) >> 15:
#                 temp_list = list(bin(self.sensor_data[1].astype(int)))
#                 for j in range(len(temp_list) - 2):
#                     if temp_list[j + 2] == '1':
#                         temp_list[j + 2] = '0'
#                     else:
#                         temp_list[j + 2] = '1'
#                 temp_list = "".join(temp_list)
#                 self.sensor_data[1] = ~ int(temp_list, 2)
#                 self.sensor_data[1] = self.sensor_data[1] / (2 ** 7)
#
#             self.sensor_data[2] = self.sensor_data[2] * 0.061
#             self.sensor_data[3] = self.sensor_data[3] * 0.061
#             self.sensor_data[4] = self.sensor_data[4] * 0.061
#
#             self.sensor_data[5] = self.sensor_data[5] / 100
#             self.sensor_data[10] = self.sensor_data[10] / 100
#
#             placeholder = "" + str(self.data_output[22:-2])
#             self.payload_gps = np.asarray(placeholder.split(','), np.str_)
#
#             gga_ind = np.where(self.payload_gps == "$GNGGA")  # find the index of GNGGA
#             if len(gga_ind[0]) != 0:
#                 # print("GGA: " + gga_ind.astype(str))
#                 try:
#                     self.sensor_data[6] = (self.payload_gps[gga_ind[0][0] + 1].astype(np.float)).astype(np.int64)
#                     self.found_gga = True
#                 except ValueError:
#                     self.found_gga = False
#             else:  # if we don't get this string, do some searching to try to get it another way
#                 for i in range(len(self.payload_gps)):
#                     if "$GNGGA" in self.payload_gps[i]:
#                         # print("STR: " + payload_gps[i])
#                         if i != len(self.payload_gps) - 1:
#                             try:
#                                 self.sensor_data[6] = (self.payload_gps[i + 1].astype(np.float)).astype(np.int64)
#                                 self.found_gga = True
#                                 # print("alt GGA: " + str(gga_ind))
#                                 break
#                             except ValueError:
#                                 pass
#             if self.found_gga:
#                 self.found_gga = False
#             else:
#                 self.sensor_data[6] = 0
#
#             NS_ind = np.where(self.payload_gps == "N")
#             if len(NS_ind[0]) != 0:
#                 if NS_ind[0][0] != 0:
#                     for i in range(len(NS_ind[0])):
#                         try:
#                             self.sensor_data[7] = (self.payload_gps[NS_ind[0][i] - 1].astype(np.float)) / 100
#                             temp_dec = self.sensor_data[7] % 1
#                             self.sensor_data[7] -= temp_dec
#                             temp_dec = (temp_dec * 100) / 60
#                             self.sensor_data[7] += temp_dec
#                         except ValueError:
#                             if i == len(NS_ind[0]) - 1:
#                                 self.sensor_data[7] = 0
#                             pass
#                 else:
#                     self.sensor_data[7] = 0
#             else:
#                 NS_ind = np.where(self.payload_gps == "S")
#                 if len(NS_ind[0]) != 0:
#                     if NS_ind[0][0] != 0:
#                         for i in range(len(NS_ind[0])):
#                             try:
#                                 # set negative if in S hemisphere
#                                 self.sensor_data[7] = (self.payload_gps[NS_ind[0][i] - 1].astype(np.float)) / 100
#                                 temp_dec = self.sensor_data[7] % 1
#                                 self.sensor_data[7] -= temp_dec
#                                 temp_dec = (temp_dec * 100) / 60
#                                 self.sensor_data[7] += temp_dec
#                                 self.sensor_data[7] = self.sensor_data[7] * -1
#                             except ValueError:
#                                 if i == len(NS_ind[0]) - 1:
#                                     self.sensor_data[7] = 0
#                                 pass
#                     else:
#                         self.sensor_data[7] = 0
#                 else:
#                     self.sensor_data[7] = 0
#
#             # ARRAY TABLE #
#             # 6 = time | 7 = GPS coords N/S | 8 = GPS coords E/W | 9 = height in m
#             EW_ind = np.where(self.payload_gps == "E")
#             if len(EW_ind[0]) != 0:
#                 if EW_ind[0][0] != 0:
#                     for i in range(len(EW_ind[0])):
#                         try:
#                             self.sensor_data[8] = (self.payload_gps[EW_ind[0][i] - 1].astype(np.float)) / 100
#                             temp_dec = self.sensor_data[8] % 1
#                             self.sensor_data[8] -= temp_dec
#                             temp_dec = (temp_dec * 100) / 60
#                             self.sensor_data[8] += temp_dec
#                         except ValueError:
#                             if i == len(EW_ind[0]) - 1:
#                                 self.sensor_data[8] = 0
#                             pass
#                 else:
#                     self.sensor_data[8] = 0
#             else:
#                 EW_ind = np.where(self.payload_gps == "W")
#                 if len(EW_ind[0]) != 0:
#                     if EW_ind[0][0] != 0:
#                         for i in range(len(EW_ind[0])):
#                             try:
#                                 # set negative if in S hemisphere
#                                 self.sensor_data[8] = (self.payload_gps[EW_ind[0][i] - 1].astype(np.float)) / 100
#                                 temp_dec = self.sensor_data[8] % 1
#                                 self.sensor_data[8] -= temp_dec
#                                 temp_dec = (temp_dec * 100) / 60
#                                 self.sensor_data[8] += temp_dec
#                                 self.sensor_data[8] = self.sensor_data[8] * -1
#                             except ValueError:
#                                 if i == len(EW_ind[0]) - 1:
#                                     self.sensor_data[8] = 0
#                                 pass
#                     else:
#                         self.sensor_data[8] = 0
#                 else:
#                     self.sensor_data[8] = 0
#
#             M_ind = np.where(self.payload_gps == "M")
#             if len(M_ind[0]) != 0:
#                 if M_ind[0][0] != 0:
#                     try:
#                         height_M = (self.payload_gps[M_ind[0][0] - 1].astype(np.float)).astype(np.int64)
#                     except ValueError:
#                         height_M = self.sensor_data[9]
#                     if height_M < 0:
#                         try:
#                             height_M = (self.payload_gps[M_ind[0][1] - 1].astype(np.float)).astype(np.int64)
#                         except ValueError:
#                             height_M = self.sensor_data[9]
#                         if height_M < 0:
#                             height_M = 0
#                 else:
#                     height_M = 0
#             else:
#                 height_M = 0
#             self.sensor_data[9] = height_M
#
#             # print("Internal Temp:   " + str(self.sensor_data[0]))
#             # print("External Temp:   " + str(self.sensor_data[1]))
#             # print("X Accel:     " + str(self.sensor_data[2]))
#             # print("Y Accel:     " + str(self.sensor_data[3]))
#             # print("Z Accel:     " + str(self.sensor_data[4]))
#             # print("Pressure:    " + str(self.sensor_data[5]))
#             # print("Time: " + str(self.sensor_data[6]))
#             # print("Latitude:  " + str(self.sensor_data[7]))
#             # print("Longitude:  " + str(self.sensor_data[8]))
#             # print("Altitude:  " + str(self.sensor_data[9]))
#             # print("Pressure Temp: " + str(self.sensor_data[10]))
#             # print("Packets sent: " + str(self.sensor_data[11]))
#             # print("Packets received " + str(self.sensor_data[12]))
#
#             ui.time_val2["text"] = str(self.sensor_data[6])
#             ui.lat_val2["text"] = str(self.sensor_data[7])
#             ui.lon_val2["text"] = str(self.sensor_data[8])
#             ui.altm_val2["text"] = str(self.sensor_data[9])
#             ui.altft_val2["text"] = str((self.sensor_data[9].astype(int) * 3.28084))
#             ui.temp1_val2["text"] = str(self.sensor_data[0])
#             ui.temp2_val2["text"] = str(self.sensor_data[1])
#             ui.tempp_val2["text"] = str(self.sensor_data[10])
#             ui.press_val2["text"] = str(self.sensor_data[5])
#             ui.x_val2["text"] = str(self.sensor_data[2])
#             ui.y_val2["text"] = str(self.sensor_data[3])
#             ui.z_val2["text"] = str(self.sensor_data[4])
#
#         return


if __name__ == "__main__":
    main_window = tk.Tk()
    ui = Window()
    ui.setup_ui(main_window)
    main_window.mainloop()
