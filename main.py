# coding=utf-8
import serial

ser = serial.Serial("COM3", 9600, timeout=1)
ser.close()
ser.open()

text = "Zkouška sériové linky"
ser.write(text.encode("utf-8"))

data = ser.readline()
print(data.decode("utf-8"))
ser.close()
