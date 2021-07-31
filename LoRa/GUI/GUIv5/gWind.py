import tkinter as tk
from tkinter import *
from tkinter import ttk
import sys


class UIWind(object):
    def setup_ui(self, main_window):
        main_window.title("LoRa UI v5")
        main_window.geometry('800x800')
        frame = Frame(main_window, padx=5, pady=5)
        frame.pack(expand=True)

        com_list_label = Label(frame, text="Select Port From List")
        com_list_label.grid(row=1, column=1)
        com_list = ttk.Combobox(frame)
        com_list.grid(row=1, column=2)
        com_select = Button(frame, text="Select")
        com_select.grid(row=1, column=3)

        sel_i2c_label = Label(frame, text="Select I2C Interface")
        sel_i2c_label.grid(row=2, column=1)
        sel_i2c_list = ttk.Combobox(frame)
        sel_i2c_list.grid(row=2, column=2)
        sel_i2c_select = Button(frame, text="Select")
        sel_i2c_select.grid(row=2, column=3)

        board_label = Label(frame, text="Board ID")
        board_label.grid(row=3, column=1)
        board_val = Label(frame, text="")
        board_val.grid(row=3, column=2)

        lat_label = Label(frame, text="Latitude")
        lat_label.grid(row=4, column=1)
        lat_val = Label(frame, text="")
        lat_val.grid(row=4, column=2)

        lon_label = Label(frame, text="Longitude")
        lon_label.grid(row=5, column=1)
        lon_val = Label(frame, text="")
        lon_val.grid(row=5, column=2)

        altm_label = Label(frame, text="Altitude")
        altm_label.grid(row=6, column=1)
        altm_val = Label(frame, text="")
        altm_val.grid(row=6, column=2)
        altm_units = Label(frame, text="meters")
        altm_units.grid(row=6, column=3)

        altft_label = Label(frame, text="Altitude")
        altft_label.grid(row=7, column=1)
        altft_val = Label(frame, text="")
        altft_val.grid(row=7, column=2)
        altft_units = Label(frame, text="feet")
        altft_units.grid(row=7, column=3)

        temp1_label = Label(frame, text="Temperature 1")
        temp1_label.grid(row=8, column=1)
        temp1_val = Label(frame, text="")
        temp1_val.grid(row=8, column=2)
        temp1_units = Label(frame, text="Celsius")
        temp1_units.grid(row=8, column=3)

        temp2_label = Label(frame, text="Temperature 2")
        temp2_label.grid(row=9, column=1)
        temp2_val = Label(frame, text="")
        temp2_val.grid(row=9, column=2)
        temp2_units = Label(frame, text="Celsius")
        temp2_units.grid(row=9, column=3)

        tempp_label = Label(frame, text="Temperature P")
        tempp_label.grid(row=10, column=1)
        tempp_val = Label(frame, text="")
        tempp_val.grid(row=10, column=2)
        tempp_units = Label(frame, text="Celsius")
        tempp_units.grid(row=10, column=3)

        press_label = Label(frame, text="Pressure")
        press_label.grid(row=11, column=1)
        press_val = Label(frame, text="")
        press_val.grid(row=11, column=2)
        press_units = Label(frame, text="milli Bar")
        press_units.grid(row=11, column=3)

        x_label = Label(frame, text="X")
        x_label.grid(row=12, column=1)
        x_val = Label(frame, text="")
        x_val.grid(row=12, column=2)
        x_units = Label(frame, text="milli g")
        x_units.grid(row=12, column=3)

        y_label = Label(frame, text="Y")
        y_label.grid(row=13, column=1)
        y_val = Label(frame, text="")
        y_val.grid(row=13, column=2)
        y_units = Label(frame, text="milli g")
        y_units.grid(row=13, column=3)

        z_label = Label(frame, text="Z")
        z_label.grid(row=14, column=1)
        z_val = Label(frame, text="")
        z_val.grid(row=14, column=2)
        z_units = Label(frame, text="milli g")
        z_units.grid(row=14, column=3)

        pack_s_label = Label(frame, text="Packets Sent")
        pack_s_label.grid(row=15, column=1)
        pack_s_val = Label(frame, text="")
        pack_s_val.grid(row=15, column=2)

        pack_r_label = Label(frame, text="Packets Received")
        pack_r_label.grid(row=16, column=1)
        pack_r_val = Label(frame, text="")
        pack_r_val.grid(row=14, column=2)

        pack_l_label = Label(frame, text="Packets Lost")
        pack_l_label.grid(row=17, column=1)
        pack_l_val = Label(frame, text="")
        pack_l_val.grid(row=14, column=2)


if __name__ == "__main__":
    main_window = tk.Tk()
    ui = UIWind()
    ui.setup_ui(main_window)
    main_window.mainloop()
