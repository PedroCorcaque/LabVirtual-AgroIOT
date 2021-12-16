import csv
import json
from datetime import date, datetime

PATH_TO_CSV_FILE = '.\data\sensors_data.csv'
HEADER = 'ID_TRANSMITTER/HUMIDITY/TIMESTAMP'

class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)
    
    def returnJson(j):
        return json.dumps(j)

def get_real_time() -> list:
    time_now = datetime.now()
    today = date.today()
    current_date = '{}-{}-{}'.format(today.day, today.month, today.year)
    current_time = time_now.strftime('%H:%M:%S')    
    return [current_date, current_time]

def check_if_file_exists(filepath: str) -> bool:
    try:
        open(filepath, 'r')
        return True
    except FileNotFoundError:
        return False

# pay = Payload
def add_line_on_file(data: bytes):
    payload = Payload(data)
    transmitter = str(payload.Transmissor)
    humidity = str(payload.Umidade)

    data = transmitter + '/' + humidity

    if '#' in data:
        data = data.replace('#','NA')
    data = data.split('/')
    data.append(get_real_time())
    
    if check_if_file_exists(PATH_TO_CSV_FILE):
        with open(PATH_TO_CSV_FILE, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data)
    else:
        data_header = HEADER.split('/')
        with open(PATH_TO_CSV_FILE, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data_header)
            writer.writerow(data)
