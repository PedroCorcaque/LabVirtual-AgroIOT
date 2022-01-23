import csv
import time
from typing import Text
import serial
import requests

porta_serial = "COM3" # Especificar porta serial a ser utilizada
baudrate = 9600
timeout = 10
url = "http://192.168.1.118:8000/"
filepath = ".\data\distance.csv"
HEADER = ["DATA","HORA","DISTANCIA_A","DISTANCIA_B"]

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

def bin2str(data_entry: bytes) -> list:
    '''
    @params
    data_entry: data in byte format

    @return
    data in string format
    '''
    count = 0
    data = data_entry.decode('utf-8')
    
    infos = data.split('+')
    infos = [str(i).replace('\r','').replace('\n','') for i in infos]
    return infos

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
        print(str(e))

def send_message(url, info):
    url = url
    print(info)
    response = requests.put(url, json={
        "_id": info[0],
        "hora": info[1],
        "dist_1": info[2],
        "dist_2": info[3]
        })

    print(response.text)

if __name__ == '__main__':
    hora_anterior = ""
    counter = 0
    while True:
        info_sensors = readSerialPort(porta_serial, baudrate, timeout)
        if hora_anterior == "":
            send_message(url, info_sensors)
            addLineOnFile(filepath, info_sensors)
            hora_anterior = info_sensors[1]
        else:
            if hora_anterior != info_sensors[1]:
                send_message(url, info_sensors)
                addLineOnFile(filepath, info_sensors)
                hora_anterior = info_sensors[1]
            else:
                continue