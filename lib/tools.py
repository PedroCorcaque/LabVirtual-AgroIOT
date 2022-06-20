import serial

def verifyArguments(**kwargs):
    operating_system = kwargs.get('operating_system')
    POSSIBLE_OS = kwargs.get('POSSIBLE_OS')
    serial_port = kwargs.get('serial_port')

    if operating_system not in POSSIBLE_OS:
        raise Exception(f'Operating System not configured. Please, use {POSSIBLE_OS}')
    if (operating_system == 'windows' and '/dev/' in serial_port) or (operating_system == 'linux' and 'COM' in serial_port):
        raise Exception(f'Serial port {serial_port} don\'t exist in this OS. Please, use port of the other system')

def readSerialPort(serial_port: str, baudrate: int):
    try:
        s = serial.Serial(serial_port, baudrate)
        return s.readline()
    except Exception as e:
        raise e