# coding=utf-8
import serial
import uuid
import time


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
                    print("Disconnected")
                    return False
                else:
                    self.ser.open()
                    # print("Connected")
                    return True
        except serial.SerialException as e:
            print("No connection! ", e)
            return "unpluged"

    def isconnected(self):
        try:
            return self.ser.isOpen()
        except serial.SerialException as e:
            return False

    def serialwrite(self, data):
        try:
            datalength = self.ser.write(data.encode())
            return datalength

        except serial.SerialException as e:
            print("Error in writing data. ", e)
            return False

    def serialread(self, datalength):
        try:
            data = self.ser.read(datalength).decode()
            return data

        except serial.SerialException as e:
            print("Error in reading data. ", e)
            return False


def main():
    ser = SerialWrapper({"port": "COM3", "baudrate": 9600})
    i = 1
    while i < 100000:
        i += 1
        if ser.isconnected():
            value = uuid.uuid4().hex
            length = ser.serialwrite(value)
            print(ser.serialread(length))
            ser.disconnect()
        else:
            status = ser.handleconnect()
            if status is "unpluged":
                while 1:
                    time.sleep(2)
                    if ser.handleconnect() is True:
                        break

    ser.disconnect()


main()
