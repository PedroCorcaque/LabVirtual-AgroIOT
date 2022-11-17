#!/usr/bin/env python3
import csv
import time
from datetime import datetime
import serial
from os import environ
from pymongo import MongoClient
import requests
from bot import telegramSendMessage
import json
import os

MAX_TEMPERATURE = float(31.0)
MIN_HUMIDITY = float(6.0)

url = "https://data.mongodb-api.com/app/data-gvnvn/endpoint/data/beta/action/updateOne"
porta_serial = "/dev/ttyUSB0" # Especificar porta serial a ser utilizada
baudrate = 9600
timeout = 10
HEADER = ["data", "hora", "umidade_a", "condutividade_a", "temperatura_a", "umidade_b", "condutividade_b", "temperatura_b"]
fila_de_leituras = []
CHAT_ID_SANTIAGO = '2052104922'
CHAT_ID_CORCAQUE = '1151737012'

def sendErrorMessage(chat_id_admin, message):

    send_text = f"https://api.telegram.org/bot5282017036:AAGZyfFSstVfdyetexitox6zjftNg2bxr0U/sendMessage?chat_id={chat_id_admin}&parse_mode=Markdown&text={message}"

    resp = requests.get(send_text)

    return resp.json()

def sendAlertBot(data: dict):
    message = ''
    HEADER = 'ALERTA\n\n'
    for temp in [data["temperaturaA"], data["temperaturaB"]]:
        if temp == None:
            continue
        else:
            if float(temp) > MAX_TEMPERATURE:
                if HEADER in message:
                    message += f'Temperatura acima do valor estabelecido ({MAX_TEMPERATURE} ºC).\nTemperatura atual: {temp} ºC.\n\n'
                else:
                    message += HEADER
                    message += f'Temperatura acima do valor estabelecido ({MAX_TEMPERATURE} ºC).\nTemperatura atual: {temp} ºC.\n\n'
    for umid in [data["umidadeA"], data["umidadeB"]]:
        if umid == None:
            continue
        else:
            if float(umid) < MIN_HUMIDITY:
                if HEADER in message:
                    message += f'Umidade abaixo do valor estabelecido ({MIN_HUMIDITY}).\nUmidade atual: {umid}.\n\n'
                else:
                    message += HEADER
                    message += f'Umidade abaixo do valor estabelecido ({MIN_HUMIDITY}).\nUmidade atual: {umid}.\n\n'
    if message != '':
        message += f'Hora da leitura: {data["hora"]}.\n'
    return message

def sendMessageBot(data):
    message = ''
    if len(data) == 7:
        # sem um dos sensores
        if data[2] == '':
            # sem sensor 1
            data = [data[0], data[1], None, None, None, data[7], data[8], data[9]]
            message += f"Data da leitura: {data[0]}\nHora da leitura: {data[1]}\n***SEM PALHA***\nUmidade: {data[2]}\nCondutividade eletrica: {data[3]}\nTemperatura: {data[4]}"
        elif data[6] == '':
            # sem sensor 2
            data = [data[0], data[1], data[3], data[4], data[5], None, None, None]
            message += f"Data da leitura: {data[0]}\nHora da leitura: {data[1]}\n***SEM PALHA***\nUmidade: {data[2]}\nCondutividade eletrica: {data[3]}\nTemperatura: {data[4]}"

    elif len(data) == 10:
        data = [data[0], data[1], data[3], data[4], data[5], data[7], data[8], data[9]]
        message += f"Data da leitura: {data[0]}\nHora da leitura: {data[1]}\n***COM PALHA***\nUmidade: {data[2]}\nCondutividade eletrica: {data[3]}\nTemperatura: {data[4]}\n***SEM PALHA***\nUmidade: {data[5]}\nCondutividade eletrica: {data[6]}\nTemperatura: {data[7]}"
    else:
        print("Erro ao receber leitura")
        raise Exception("Erro ao receber leitura")

    if message != '':
        return telegramSendMessage(message)

def checkIfFileExists(filepath: str) -> bool:
    try:
        open(filepath, 'r')
        return True
    except FileNotFoundError:
        return False    

def addLineOnFile(filepath: str, data: str) -> bool:
    if len(data) == 7:
        # sem um dos sensores
        if data[2] == '':
            # sem sensor 1
            data = [data[0], data[1], None, None, None, data[7], data[8], data[9]]
        elif data[6] == '':
            # sem sensor 2
            data = [data[0], data[1], data[3], data[4], data[5], None, None, None]
    elif len(data) == 10:
        data = [data[0], data[1], data[3], data[4], data[5], data[7], data[8], data[9]]
    else:
        print("Erro ao receber leitura")
        raise Exception("Erro ao receber leitura")

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
    return [str(i).replace('\r','').replace('\n','') for i in infos]

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

def send_request(enviar):
    payload = json.dumps({
        "collection": "Dados_Sensores",
        "database": "DBLabvirtual",
        "dataSource": "LabvitualData",
        'filter':{
            '_id': enviar['data']
        },
        "update": {
            '$push': {
                'hora': enviar['hora'],
                'sensor.A.Umidade': enviar['umidadeA'],
                'sensor.A.Condutividade': enviar['condutividadeA'],
                'sensor.A.Temperatura': enviar['temperaturaA'],
                'sensor.B.Umidade': enviar['umidadeB'],
                'sensor.B.Condutividade': enviar['condutividadeB'],
                'sensor.B.Temperatura': enviar['temperaturaB'],
            },
        },
        'upsert': True
    })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'kG7FLPGRlWolLdfJEgxJQtibU4CGvaetuVqRmTgI3wGm4SeyCr8MLsah9ERUufNw'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.status_code

def make_request(enviar):
    if fila_de_leituras:
        erro = False
        # print(f'Acessando algoritmo de fila...')
        fila_de_leituras.append(enviar)
        # print(f'Tamanho da fila: {len(fila_de_leituras)}')
        for leitura in fila_de_leituras:
            status_code = send_request(enviar)
            if status_code == 200 or status_code == 201:
                print(f'Leitura {len(fila_de_leituras)} enviada com sucesso.')
                continue
            else:
                print(f'Ainda sem conexão, algoritmo de fila continuando...')        
                erro = True
                break
        if erro == False:
            fila_de_leituras.clear()
            print(f'Toda fila foi acessada e enviada ao banco.')
    else:
        # resp = requests.put("https://apilabvirtual.loca.lt/", json=enviar)
        status_code = send_request(enviar)
        if status_code == 200 or status_code == 201:
            print('Leitura enviada com sucesso.')
            # print('-----------------------')
            # print(f'Hora: {enviar["hora"]}\n---Sem palha---\nUmidade: {enviar["umidadeB"]}\nCond. Elet.: {enviar["condutividadeB"]}\nTemp.: {enviar["temperaturaB"]}\n---Com palha---\nUmidade: {enviar["umidadeA"]}\nCond. Elet.: {enviar["condutividadeA"]}\nTemp.: {enviar["temperaturaA"]}\n')
        else:
            fila_de_leituras.append(enviar)
            print(f'Status: {status_code}\nIniciando algoritmo de fila...')

def send_message(data_received):
    if len(data_received) == 7:
    # sem um dos sensores
        if data_received[2] == '':
            # sem sensor 1
            data_to_send = [data_received[0], data_received[1], None, None, None, data_received[7], data_received[8], data_received[9]]
        elif data_received[6] == '':
            # sem sensor 2
            data_to_send = [data_received[0], data_received[1], data_received[3], data_received[4], data_received[5], None, None, None]

        enviar = {
            "data": data_to_send[0],
            "hora": data_to_send[1],
            "umidadeA": float(data_to_send[2]),
            "condutividadeA": float(data_to_send[3]),
            "temperaturaA": float(data_to_send[4]),
            "umidadeB": float(data_to_send[5]),
            "condutividadeB":float(data_to_send[6]),
            "temperaturaB": float(data_to_send[7])
        }

        try:
            msg = sendAlertBot(enviar)
            if msg != '':
                telegramSendMessage(msg)
        except Exception as e:
            pass
        make_request(enviar)

    elif len(data_received) == 10:
        data_to_send = [data_received[0], data_received[1], data_received[3], data_received[4], data_received[5], data_received[7], data_received[8], data_received[9]]

        enviar = {
            "data": data_to_send[0],
            "hora": data_to_send[1],
            "umidadeA": float(data_to_send[2]),
            "condutividadeA": float(data_to_send[3]),
            "temperaturaA": float(data_to_send[4]),
            "umidadeB": float(data_to_send[5]),
            "condutividadeB":float(data_to_send[6]),
            "temperaturaB": float(data_to_send[7])
        }

#         import requests
# import json
# url = "https://data.mongodb-api.com/app/data-gvnvn/endpoint/data/beta/action/updateOne"

# payload = json.dumps({
#     "collection": "teste",
#     "database": "DBLabvirtual",
#     "dataSource": "LabvitualData",
#     'filter':{
#         '_id': 'testeID'
#     },
#     "update": {
#         '$push': {
# 			'hora': 'teste',
# 			'sensor.A.Umidade': 'teste',
# 			'sensor.A.condutividade': 'teste',
# 			'sensor.A.Temperatura': 'teste',
# 			'sensor.B.Umidade': 'teste',
# 			'sensor.B.condutividade': 'teste',
# 			'sensor.B.Temperatura': 'teste',
# 		},
#     },
#     'upsert': True
# })
# headers = {
#     'Content-Type': 'application/json',
#     'Access-Control-Request-Headers': '*',
#     'api-key': 'kG7FLPGRlWolLdfJEgxJQtibU4CGvaetuVqRmTgI3wGm4SeyCr8MLsah9ERUufNw'
# }

# response = requests.request("POST", url, headers=headers, data=payload)


        try:
            msg = sendAlertBot(enviar)
            if msg != '':
                telegramSendMessage(msg)
        except Exception as e:
            pass

        print('Vai mandar em')
        make_request(enviar)
        print('Mandou')
    else:
        print("Erro ao receber leitura")
        # print(data_received)
        
        raise Exception("Erro ao receber leitura")


    # db = MongoClient(environ['CORC_MONGO_USER'])['DBLabvirtual']['Dados_Sensores']

    # db.update_one({'_id': data[0]}, {
    # '$push':{
    #     'hora': data[1],
    #     'sensor.A.Umidade': data[2],
    #     'sensor.A.condutividade': data[3],
    #     'sensor.A.Temperatura': data[4],
    #     'sensor.B.Umidade': data[5],
    #     'sensor.B.condutividade': data[6],
    #     'sensor.B.Temperatura': data[7]
    #     }}, upsert=True)

    # print(data_to_send)
    
def main():
    
    while True:
        try:
            data_read = readSerialPort(porta_serial, baudrate, delay=100)
            print(data_read)
            filename = "../data/" + data_read[0].replace("/","-") + ".csv"
            try:
                addLineOnFile(filename, data_read)
            except Exception as e:
                pass
            try:
                send_message(data_read)
            except Exception as e:
                pass
            try:
                hora = str(data_read[1])
                if hora == '23:50':
                    os.system(f'cp {filename} /run/user/1000/gvfs/google-drive:host=gmail.com,user=lvunipampa')
            except Exception as e:
                pass
            # try:
            #     sendMessageBot(data_read)
            # except Exception as e:
            #     pass

            time.sleep(72)
        except Exception as e:
            print(str(e))
            


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Error: {str(e)}\n')
        print(f'\nTrying again in {timeout} seconds...')
        time.sleep(timeout)
        main()
    
