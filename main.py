# coding=utf-8
import serial
import time
from random import randint


class SerialWrapper:

    def __init__(self, settings):
        self.ser = None
        self.settings = settings
        self.handleconnect()

    def disconnect(self):
        self.ser.close()

    def handleconnect(self):
        try:
            if self.ser is None:
                self.ser = serial.Serial(self.settings["port"], self.settings["baudrate"])
                self.ser.close()
                self.ser.open()
                print("Successfully connected to port %r." % self.ser.port)
                return True
            else:
                if self.ser.isOpen():
                    self.ser.close()
                    self.ser = None
                    return False
                else:
                    self.ser.open()
                    return True
        except serial.SerialException as e:
            print("No connection! ", e)
            return "unplugged"

    def isconnected(self):
        try:
            return self.ser.isOpen()
        except serial.SerialException as e:
            return False

    def serialwrite(self, data):
        try:
            return self.ser.write(data.encode())

        except serial.SerialException as e:
            print("Error in writing data. ", e)
            return False

    def serialread(self, datalength):
        try:
            return self.ser.read(datalength).decode()

        except serial.SerialException as e:
            print("Error in reading data. ", e)
            return False

    def readline(self):
        try:
            return self.ser.readline().decode()

        except serial.SerialException as e:
            print("Error in reading line. ", e)
            return False


def shut_down_leds(ser_instance):
    ser_instance.serialwrite("W010000XXXX\r")
    ser_instance.serialwrite("W020000XXXX\r")


def run_even(ser_instance):
    print("Turning on even leds for 4 seconds")
    ser_instance.serialwrite("W015555XXXX\r")
    ser_instance.serialwrite("W025555XXXX\r")
    time.sleep(4)
    shut_down_leds(ser_instance)
    print("Done")


def run_odd(ser_instance):
    print("Turning on even leds for 4 seconds")
    ser_instance.serialwrite("W01AAAAXXXX\r")
    ser_instance.serialwrite("W02AAAAXXXX\r")
    time.sleep(4)
    shut_down_leds(ser_instance)
    print("Done")


def run_all(ser_instance):
    print("Turning on all leds for 4 seconds")
    ser_instance.serialwrite("W01FFFFXXXX\r")
    ser_instance.serialwrite("W02FFFFXXXX\r")
    time.sleep(4)
    shut_down_leds(ser_instance)
    print("Done")


def run_random(ser_instance):
    print("Turning on random leds in 15 cycles")
    i = 0
    while i < 15:
        i += 1
        w1_rand = randint(0, 65536)
        w2_rand = randint(0, 65536)
        ser_instance.serialwrite("W01" + format(w1_rand, "04x") + "XXXX\r")
        ser_instance.serialwrite("W02" + format(w2_rand, "04x") + "XXXX\r")
        time.sleep(0.4)
    shut_down_leds(ser_instance)
    print("Done")


def run_custom(ser_instance):
    custom = input("Enter custom combination: ")
    custom = custom.split(",")
    if isinstance(custom, list):
        if len(custom[0]) == 4 and len(custom[1]) == 4:
            ser_instance.serialwrite("W01" + format(custom[0], "04x") + "XXXX\r")
            ser_instance.serialwrite("W02" + format(custom[1], "04x") + "XXXX\r")
            print("Done")
        elif custom[0] == "1" and len(custom[1]) == 4:
            ser_instance.serialwrite("W01" + custom[1] + "XXXX\r")
            print("Done")
        elif custom[0] == "2" and len(custom[1]) == 4:
            ser_instance.serialwrite("W02" + custom[1] + "XXXX\r")
            print("Done")
        else:
            print("Bad format")
            run_custom(ser_instance)
    else:
        print("Bad format")
        run_custom(ser_instance)


def program_select():
    print("Available programs:")
    print("1) Turn on even leds for 4 seconds")
    print("2) Turn on odd leds for 4 seconds")
    print("3) Turn on all leds for 4 seconds")
    print("4) Turn on random leds in 15 cycles")
    print("5) Enter custom leds combination in hexa for one or both cards, separated with comma.")
    print("    - For both cards: FFFF,FFFF")
    print("    - For one card: 1,FFFF or 2,FFFF")
    return input("Enter program number: ")


run = True
port_name = input("Enter port name (COM3): ")
ser = SerialWrapper({"port": port_name, "baudrate": 115200})
ser.serialwrite("W010000XXXX\r")
ser.serialwrite("W020000XXXX\r")

while run:
    if ser.isconnected():
        program_number = program_select()
        print(" ")

        if program_number == "1":
            run_even(ser)
        elif program_number == "2":
            run_odd(ser)
        elif program_number == "3":
            run_all(ser)
        elif program_number == "4":
            run_random(ser)
        elif program_number == "5":
            run_custom(ser)
        else:
            print("Bad number")

        ser.disconnect()
        next_step = input("Continue? To quit, enter 'exit': ")
        print(" ")
        if next_step == "exit":
            print("Exiting program...")
            run = False
    else:
        status = ser.handleconnect()
        if status is "unplugged":
            while 1:
                time.sleep(2)
                if ser.handleconnect() is True:
                    break

ser.disconnect()
