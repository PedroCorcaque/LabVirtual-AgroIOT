import os
import requests

bot_token = os.environ["telegram_bot_token"]
chat_id = '-643476646'

def getChatID():
    resp = requests.get(f"https://api.telegram.org/bot{bot_token}/getUpdates")
    print(resp.content)

def telegramSendMessage(message):
    send_text = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}"

    resp = requests.get(send_text)

    return resp.json()

if __name__ == '__main__':
    valor = 10
    message = f"Data da leitura: {valor}\nHora da leitura: {valor}\n***SEM PALHA***\nUmidade: {valor}\nCondutividade eletrica: {valor}\nTemperatura: {valor}"
    telegramSendMessage(message)