import serial
import serial.tools.list_ports

# print all ports
ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))

ser = serial.Serial('COM9')  # open serial port
print(ser.name)         # check which port was really used

ser.write('Hello World\n'.encode())

while True:
    if ser.inWaiting():
        print(ser.read_all().decode())

ser.close()