import argparse

from lib.tools import *

POSSIBLE_OS = ['linux', 'windows']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This software')
    parser.add_argument('-os', '--operating_system', type=str, default='linux', help='The SO the software will be used. Possible OS: linux or windows')
    parser.add_argument('-s', '--serial_port', type=str, default='/dev/ttyUSB0', help='The serial port the arduino is connected. Example for Windows: COM0, COM1, ... Example for Linux: /dev/ttyUSB[0-9], /dev/ttyACM[0-9]')
    args = vars(parser.parse_args())

    operating_system = args['operating_system'].lower()
    serial_port = args['serial_port']

    verifyArguments(operating_system=operating_system, serial_port=serial_port, POSSIBLE_OS=POSSIBLE_OS)

    data = readSerialPort(serial_port=serial_port, baudrate=9600)