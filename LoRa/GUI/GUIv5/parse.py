import numpy as np


class Parse(object):
    def __init__(self, ui):
        self.data_output = np.zeros(500)
        self.board = ui.board
        self.running = ui.running
        self.data_stream = ""
        # print("Board1Thread INIT")
        self.sensor_data = np.zeros(500)
        self.payload_gps = np.zeros(500)
        self.found_gga = False
        self.system_running()

    def system_running(self):
        while self.running:
            self.data_stream = self.board.rec_data()
            # test = 0
            # while test != '[':
            #     try:
            #         test = self.board.rec_data().decode("utf-8")
            #         # if test == '[':
            #         #     print("YES")
            #         #     start_flag = True
            #     except:
            #         pass
            #         # print("couldn't decode character (this is okay)")  # This line can be used for debug if desired

            char = self.board.rec_data().decode("utf-8")
            string_rec = char
            while char != ']':
                char = self.board.rec_data().decode("utf-8")
                if char != ']' or '':
                    string_rec = string_rec + char
                # print(string_rec)
            self.data_output = np.asarray(string_rec.split(','))
            # print(self.data_output)

            # rssi_snr = self.data_output[-2:]
            # self.data_output = self.data_output[-2:].astype(int)

            self.sensor_data[0] = (self.data_output[1].astype(int) << 8) + self.data_output[2].astype(
                int)  # set internal temp
            self.sensor_data[1] = (self.data_output[3].astype(int) << 8) + self.data_output[4].astype(
                int)  # set external temp
            self.sensor_data[2] = (self.data_output[5].astype(int) << 8) + self.data_output[6].astype(
                int)  # set accel x
            self.sensor_data[3] = (self.data_output[7].astype(int) << 8) + self.data_output[8].astype(
                int)  # set accel y
            self.sensor_data[4] = (self.data_output[9].astype(int) << 8) + self.data_output[10].astype(
                int)  # set accel z
            self.sensor_data[5] = (self.data_output[11].astype(int) << 24) + (
                    (self.data_output[12].astype(int) << 16) + (self.data_output[13].astype(int) << 8) + (
                        self.data_output[14].astype(int)))
            self.sensor_data[10] = (self.data_output[15].astype(int) << 24) + (
                    (self.data_output[16].astype(int) << 16) + (self.data_output[17].astype(int) << 8) + (
                        self.data_output[18].astype(int)))
            self.sensor_data[11] = (self.data_output[19].astype(int) << 8) + self.data_output[20].astype(int)

            if self.sensor_data[0].astype(int) >> 15:
                temp_list = list(bin(self.sensor_data[0].astype(int)))
                for j in range(len(temp_list) - 2):
                    if temp_list[j + 2] == '1':
                        temp_list[j + 2] = '0'
                    else:
                        temp_list[j + 2] = '1'
                temp_list = "".join(temp_list)
                self.sensor_data[0] = ~ int(temp_list, 2)
                self.sensor_data[0] = self.sensor_data[0] / (2 ** 7)

            if self.sensor_data[1].astype(int) >> 15:
                temp_list = list(bin(self.sensor_data[1].astype(int)))
                for j in range(len(temp_list) - 2):
                    if temp_list[j + 2] == '1':
                        temp_list[j + 2] = '0'
                    else:
                        temp_list[j + 2] = '1'
                temp_list = "".join(temp_list)
                self.sensor_data[1] = ~ int(temp_list, 2)
                self.sensor_data[1] = self.sensor_data[1] / (2 ** 7)

            self.sensor_data[2] = self.sensor_data[2] * 0.061
            self.sensor_data[3] = self.sensor_data[3] * 0.061
            self.sensor_data[4] = self.sensor_data[4] * 0.061

            self.sensor_data[5] = self.sensor_data[5] / 100
            self.sensor_data[10] = self.sensor_data[10] / 100

            placeholder = "" + str(self.data_output[22:-2])
            self.payload_gps = np.asarray(placeholder.split(','), np.str_)

            gga_ind = np.where(self.payload_gps == "$GNGGA")  # find the index of GNGGA
            if len(gga_ind[0]) != 0:
                # print("GGA: " + gga_ind.astype(str))
                try:
                    self.sensor_data[6] = (self.payload_gps[gga_ind[0][0] + 1].astype(np.float)).astype(
                        np.int64)
                    self.found_gga = True
                except ValueError:
                    self.found_gga = False
            else:  # if we don't get this string, do some searching to try to get it another way
                for i in range(len(self.payload_gps)):
                    if "$GNGGA" in self.payload_gps[i]:
                        # print("STR: " + payload_gps[i])
                        if i != len(self.payload_gps) - 1:
                            try:
                                self.sensor_data[6] = (self.payload_gps[i + 1].astype(np.float)).astype(
                                    np.int64)
                                self.found_gga = True
                                # print("alt GGA: " + str(gga_ind))
                                break
                            except ValueError:
                                pass
            if self.found_gga:
                self.found_gga = False
            else:
                self.sensor_data[6] = 0

            ns_ind = np.where(self.payload_gps == "N")
            if len(ns_ind[0]) != 0:
                if ns_ind[0][0] != 0:
                    for i in range(len(ns_ind[0])):
                        try:
                            self.sensor_data[7] = (self.payload_gps[ns_ind[0][i] - 1].astype(np.float)) / 100
                            temp_dec = self.sensor_data[7] % 1
                            self.sensor_data[7] -= temp_dec
                            temp_dec = (temp_dec * 100) / 60
                            self.sensor_data[7] += temp_dec
                        except ValueError:
                            if i == len(ns_ind[0]) - 1:
                                self.sensor_data[7] = 0
                            pass
                else:
                    self.sensor_data[7] = 0
            else:
                ns_ind = np.where(self.payload_gps == "S")
                if len(ns_ind[0]) != 0:
                    if ns_ind[0][0] != 0:
                        for i in range(len(ns_ind[0])):
                            try:
                                # set negative if in S hemisphere
                                self.sensor_data[7] = (self.payload_gps[ns_ind[0][i] - 1].astype(
                                    np.float)) / 100
                                temp_dec = self.sensor_data[7] % 1
                                self.sensor_data[7] -= temp_dec
                                temp_dec = (temp_dec * 100) / 60
                                self.sensor_data[7] += temp_dec
                                self.sensor_data[7] = self.sensor_data[7] * -1
                            except ValueError:
                                if i == len(ns_ind[0]) - 1:
                                    self.sensor_data[7] = 0
                                pass
                    else:
                        self.sensor_data[7] = 0
                else:
                    self.sensor_data[7] = 0

            # ARRAY TABLE #
            # 6 = time | 7 = GPS coords N/S | 8 = GPS coords E/W | 9 = height in m
            ew_ind = np.where(self.payload_gps == "E")
            if len(ew_ind[0]) != 0:
                if ew_ind[0][0] != 0:
                    for i in range(len(ew_ind[0])):
                        try:
                            self.sensor_data[8] = (self.payload_gps[ew_ind[0][i] - 1].astype(np.float)) / 100
                            temp_dec = self.sensor_data[8] % 1
                            self.sensor_data[8] -= temp_dec
                            temp_dec = (temp_dec * 100) / 60
                            self.sensor_data[8] += temp_dec
                        except ValueError:
                            if i == len(ew_ind[0]) - 1:
                                self.sensor_data[8] = 0
                            pass
                else:
                    self.sensor_data[8] = 0
            else:
                ew_ind = np.where(self.payload_gps == "W")
                if len(ew_ind[0]) != 0:
                    if ew_ind[0][0] != 0:
                        for i in range(len(ew_ind[0])):
                            try:
                                # set negative if in S hemisphere
                                self.sensor_data[8] = (self.payload_gps[ew_ind[0][i] - 1].astype(
                                    np.float)) / 100
                                temp_dec = self.sensor_data[8] % 1
                                self.sensor_data[8] -= temp_dec
                                temp_dec = (temp_dec * 100) / 60
                                self.sensor_data[8] += temp_dec
                                self.sensor_data[8] = self.sensor_data[8] * -1
                            except ValueError:
                                if i == len(ew_ind[0]) - 1:
                                    self.sensor_data[8] = 0
                                pass
                    else:
                        self.sensor_data[8] = 0
                else:
                    self.sensor_data[8] = 0

            m_ind = np.where(self.payload_gps == "M")
            if len(m_ind[0]) != 0:
                if m_ind[0][0] != 0:
                    try:
                        height_m = (self.payload_gps[m_ind[0][0] - 1].astype(np.float)).astype(np.int64)
                    except ValueError:
                        height_m = self.sensor_data[9]
                    if height_m < 0:
                        try:
                            height_m = (self.payload_gps[m_ind[0][1] - 1].astype(np.float)).astype(np.int64)
                        except ValueError:
                            height_m = self.sensor_data[9]
                        if height_m < 0:
                            height_m = 0
                else:
                    height_m = 0
            else:
                height_m = 0
            self.sensor_data[9] = height_m

            # print("Internal Temp:   " + str(self.sensor_data[0]))
            # print("External Temp:   " + str(self.sensor_data[1]))
            # print("X Accel:     " + str(self.sensor_data[2]))
            # print("Y Accel:     " + str(self.sensor_data[3]))
            # print("Z Accel:     " + str(self.sensor_data[4]))
            # print("Pressure:    " + str(self.sensor_data[5]))
            # print("Time: " + str(self.sensor_data[6]))
            # print("Latitude:  " + str(self.sensor_data[7]))
            # print("Longitude:  " + str(self.sensor_data[8]))
            # print("Altitude:  "+ str(self.sensor_data[9]))
            # print("Pressure Temp: " + str(self.sensor_data[10]))
            # print("Packets sent: " + str(self.sensor_data[11]))
            # print("Packets received " + str(self.sensor_data[12]))

            # ui.time_val["text"] = str(self.sensor_data[6])
            # ui.lat_val["text"] = str(self.sensor_data[7])
            # ui.lon_val["text"] = str(self.sensor_data[8])
            # ui.altm_val["text"] = str(self.sensor_data[9])
            # ui.altft_val["text"] = str((self.sensor_data[9].astype(int) * 3.28084))
            # ui.temp1_val["text"] = str(self.sensor_data[0])
            # ui.temp2_val["text"] = str(self.sensor_data[1])
            # ui.tempp_val["text"] = str(self.sensor_data[10])
            # ui.press_val["text"] = str(self.sensor_data[5])
            # ui.x_val["text"] = str(self.sensor_data[2])
            # ui.y_val["text"] = str(self.sensor_data[3])
            # ui.z_val["text"] = str(self.sensor_data[4])

        return self.sensor_data
