import csv
import time
import serial

filepath = '.\data\sensors_data.csv'
HEADER = 'A_Umidade,A_Condutividade,A_Temperatura,B_Umidade,B_Condutividade,B_Temperatura'

porta_serial = "COM4" # Especificar porta serial a ser utilizada
baudrate = 9600
timeout = 10

def bin2str(data_entry: bytes) -> str:
    '''
    @params
    data_entry: data in byte format

    @return
    data in string format
    '''
    count = 0
    data = data_entry.decode('utf-8')
    
    lines = data.split('\n')
    for line in lines:
        print(line)
        
    

def readSerialPort(porta_serial: str, baudrate: int, delay: int) -> str:
    '''
    @params
    porta_serial: serial port name to read
    baudrate: serial port speed
    delay: time of seconds between readings

    @return
    data: data in string format
    '''
    try:
        s = serial.Serial(porta_serial, baudrate)

        reading = ''
        reading = s.readline()
        
        if reading == '':
            time.sleep(delay)
        
        return bin2str(reading)
    except Exception as e:
        raise e

def checkIfFileExists(filepath: str) -> bool:
    try:
        open(filepath, 'r')
        return True
    except FileNotFoundError:
        return False

def addLineOnFile(filepath: str, data: str) -> bool:
    if checkIfFileExists(filepath):
        with open(filepath, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data)
    else:
        print('\nFile not exist. Making a new file...')
        with open(filepath, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(HEADER)
            writer.writerow(data)

def main():
    while True:
        data_read = readSerialPort(porta_serial, baudrate, delay=100)
        # print(data_read)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Error: {str(e)}\n')
        print('\nTrying again in {timeout} seconds...')
        time.sleep(timeout)
        main()
    
