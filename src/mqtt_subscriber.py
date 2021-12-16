import paho.mqtt.client as mqtt 

from data_entry import add_line_on_file

# Using this library: https://github.com/eclipse/paho.mqtt.python

def on_connect(client, userData, flags, resultCode):
    print('Connected with result code ' + str(resultCode))
    client.subscribe('BCICounter')

def on_message(client, userData, message):
    topic = message.topic
    payload = message.payload
    print('Mensagem recebida: {}'.format(payload))
    print('Adicionando linha no arquivo...')
    add_line_on_file(payload)
    print('Pronto.')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('mqtt.eclipseprojects.io', 1883)

client.loop_forever()