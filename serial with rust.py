import usb_cdc, time

ser = usb_cdc.data
ser.reset_input_buffer()

def recieveData(ser):
    print('starting')
    message = ser.readline().decode()[:-1]
    print(message)
    
while True:
    if ser.in_waiting > 0:
        recieveData(ser)
    time.sleep(0.01)