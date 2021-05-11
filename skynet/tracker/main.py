#!/usr/bin/env python
"""
Balloon Tracking Software for MSGC Ground Station X

Author:	Larson Dean Brandstetter, CpE
Based on work from Adam Wulfing, CpE, Austin Langford, AEM, Scott Miller, CpE, Dylan Trafford, CpE,
    and David Schwerr, CS of the Minnesota/Montana Space Grant Consortia
Software created for use by the National Space Grant Consortium
Purpose: To acquire the location of a balloon in flight, and aim the array of antennae at the balloon
Creation Date: Spring 2021

Special Thanks and Historical Contributors: Andy Kirby, CpE; Sierra MacLeod, CpE; Cayden Seiler, CpE;
    Michelle Valentino-Manno, CpE; Andrew Snider, EE; Adam Wulfing, CpE; Austin Langford, AEM; Scott Miller, CpE;
    Dylan Trafford, CpE; and David Schwerr, CS of the Minnesota/Montana Space Grant Consortia

This code was built using some parts of the original Antenna-Tracker software written by Trevor Gahl, CpE

Last Edit Date: May 11, 2021

"""

# System imports
import sys
import os
import time as t
from datetime import *
import serial
import serial.tools.list_ports

class SerialDevice:
    """ A class to manage serial devices """

    def __init__(self, port, baud, timeout):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.device = serial.Serial(
            port=self.port, baudrate=self.baud, timeout=self.timeout)

    def getPort(self):
        return self.port

    def getBaud(self):
        return self.baud

    def getTimeout(self):
        return self.timeout

    def getDevice(self):
        return self.device

class main:
    print("Looking For Arduino")
    def getSettings(self):

        for each in ports:
            print(each)
            eachLst = str(each).split('-')
            # The Arduino shows up as Arduino Uno
            if (eachLst[1].find("Arduino Uno") != -1) or (each.pid == 67):
                arduinoCOM = eachLst[0].strip()
                self.arduinoCOM.setText(arduinoCOM)

        print("Looking For Arduino")
        arduinoCOM = str(self.arduinoCOM.text())
        self.arduino = SerialDevice(arduinoCOM, 115200, 5)

        print(self.arduino)