import tkinter as tk
from tkinter import *
import sys


class UIWind(object):
    def setup_ui(self, main_window):
        main_window.title("LoRa UI v5")
        main_window.geometry('800x800')
        frame = Frame(
            main_window,
            padx=5,
            pady=5
        )
        frame.pack(expand=True)

        com_list = Combobox(
            frame,

        )

        board_id = Label(
            frame,
            text="Board ID"
        )
        board_id.grid(row=1, column=1)


if __name__ == "__main__":
    main_window = tk.Tk()
    ui = UIWind()
    ui.setup_ui(main_window)
    main_window.mainloop()
