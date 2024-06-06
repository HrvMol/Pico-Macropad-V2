import serial
import json
import hashlib

def read(port, file):
    retrieved = False

    send = f'get\n{file}\n'.encode()
    checksum = createHash(send)
    send = send + checksum + b'\r\n'
    print(send)

    ser = serial.Serial(port)
    ser.write(send)

    while retrieved == False:
        if ser.inWaiting():
            message = retreiveAll(ser)
            print(message)
            # handle checksum error
            if message.splitlines()[0] == b'AGAIN':
                ser.write(send)

            if message.splitlines()[0] == b'OK':
                print('All OK')
    
    print('recieved')
    ser.close()
    return data

def write(port, data, endLocation):
    # checks if endLocation is a json file
    if endLocation.split('.')[1] == 'json':
        try:
            print(endLocation.split('.')[1])

            ser = serial.Serial(port)
            ser.write(f'set\n{endLocation}\n{json.dumps(data)}\r\n'.encode())
            ser.close()
        except ValueError:
            pass

    elif data.split('.')[1] == 'bmp' and endLocation.split('.')[1] == 'bmp':
        f = open(data, 'rb')
        image = f.read()
        f.close()

        ser = serial.Serial(port)
        ser.write(f'set\n{endLocation}\n'.encode() + image + b'\r\n')
        ser.close()

def remove(port, file):
    retrieved = False
    ser = serial.Serial(port)
    ser.write(f'delete\n{file}\r\n'.encode())

    while retrieved == False:
        if ser.inWaiting():
            data = ser.readline()
            retrieved = True
    
    print(data)
    ser.close()

def createHash(data):
    sha = hashlib.sha1()
    sha.update(data)
    print(sha.digest())
    return sha.digest()

def retreiveAll(ser):
    end = False
    byte_array = bytearray()

    while end == False:
        line = ser.readline()
        if line[-2:-1] == b'\r':
            print('End')
            end = True
            line = line[:-2]
        byte_array.extend(line)
    return bytes(byte_array)

# remove('COM9', 'test.json')

data = read('COM9', 'pages.json')
print(data)
# write('COM9', data, 'test.json')

# write('COM9', 'acc-cycle-wipers.bmp', '/images/test.bmp')

# delete('COM9', '/images/test.bmp')

# delete('COM9', 'pages.json')