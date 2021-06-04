# from flask import Flask, request
# from gunicorn import app
import requests
import json
from wabot_Almaz import WABot, APIUrl, token
# from flask_gunicorn import
# import ast
import time
# from requests.auth import HTTPBasicAuth
# import sqlite3
# from multiprocessing import Process
# from cloudpayments import CloudPayments
# client = CloudPayments('pk_eec792a048a7d7b8c6b6e84022abf', '758a780e9689de0ffb0fd77749f23672')
conn = None#sqlite3.connect('database.db')
# cursor = conn.cursor()

# app = wsgi.app

# app = Flask(__name__)
history = dict()
carts = dict()
clients = {}
zz = []

def send_telegram(text: str):
    token = "1832470032:AAH-RVl2FE6PeVmoVo6iR0OFnbcArNWtLg8"
    url = "https://api.telegram.org/bot"
    channel_id = "498516666"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

# context = SSL.Context(SSL.SSLv23_METHOD)
def send_text(phone,text):
    if len(phone) == 10:
        phone = '7' + phone

    url = APIUrl + 'sendMessage/' + token

    payload = {"chatId": phone + '@c.us',
               "message": text}
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    return ""

def get_notifications(token):
    url = APIUrl + 'ReceiveNotification/' + token
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.text:
        return response.json()

def del_notifications(token,receipt):
    url = APIUrl + 'DeleteNotification/' + token + "/" + str(receipt)

    payload = {}
    headers = {}

    response = requests.request("DELETE", url, headers=headers, data=payload)

    print(response.text)

def get_notificationsQR(token):

    url = "https://api.green-api.com/waInstance9159/ReceiveNotification/" + token

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.text:
        return response.json()

def reset_calls(token):
    json_data = get_notifications(token)
    if json_data == None:
        return

    receipt = json_data.get('receiptId')
    if receipt:
        del_notifications(token, receipt)

def primera():
    # send_text(token,'77071392125','Start')
    reset_calls(token)
    clients = {}
    # commands = ['ZAKAZ','1', '1',  '1', '32', 'Маресьева', '95']#, '1', '3']#, '3','Вавилова','1','25','0']
    # commands = ['ZAKAZ','1', '1',  'Юрий тест', '56', 'Жубановых', '176']#, '1', '3']#, '3','Вавилова','1','25','0']
    # commands = ['ZAKAZ']
    # number_client = '79957745448'
    # cx_test = len(commands)
    # for c in commands:
    #       print('Command:',c)
    #       Body = {'typeWebhook': 'incomingMessageReceived',
    #               'instanceData': {'idInstance': 9102, 'wid': '77717919485@c.us', 'typeInstance': 'whatsapp'},
    #               'timestamp': 1616138603, 'idMessage': '3EB00939A99DB774DE89',
    #               'senderData': {'chatId': number_client+'@c.us', 'sender': '77071392125@c.us', 'senderName': 'Юрич'},
    #               'messageData': {'typeMessage': 'textMessage', 'textMessageData': {'textMessage': c}}}
    #       bot = WABot(Body, clients, conn)
    #       bot.processing(True)
    #       time.sleep(1)
    # # while True:
    #     c = input()
    #     Body = {'typeWebhook': 'incomingMessageReceived', 'instanceData': {'idInstance': 9102, 'wid': '77717919485@c.us', 'typeInstance': 'whatsapp'}, 'timestamp': 1616138603, 'idMessage': '3EB00939A99DB774DE89', 'senderData': {'chatId': number_client+'@c.us', 'sender': number_client+'@c.us', 'senderName': 'Юрич'}, 'messageData': {'typeMessage': 'textMessage', 'textMessageData': {'textMessage': c}}}
    #     bot = WABot(Body, clients, conn)
    #     bot.processing(True)
    send_telegram('Запуск')
    while True:

        json = get_notifications(token)
        if json == None:
            print('нет ответа')
            continue

        receipt = json['receiptId']
        body = json['body']
        try:
            if body['messageData']['typeMessage'] == 'textMessage':
                bot = WABot(body, clients, conn)
                bot.processing()
        except Exception as ex:
            # errorText =  f" команда: {body['messageData']['textMessageData']['textMessage']} \n" + ex
            print(ex)
            send_telegram(ex)


        if receipt:
            del_notifications(token, receipt)


if(__name__) == '__main__':
    primera()
    # segundo()
    # lsOrders = get_client_orders('7071392125', self.database['conn'].cursor)
    # p1 = Process(target=primera)
    # p2 = Process(target=segundo)
    #
    # p1.start()
    # p2.start()
    #
    # p1.join()
    # p2.join()
