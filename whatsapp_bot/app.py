# -*- coding: utf-8 -*-
import os
import time
from loguru import logger
import requests
import json
import psutil
# from wabot_Almaz import WABot, APIUrl, token
from wabot_Almaz_mini import WABot, APIUrl, token
history = dict()
carts = dict()
clients = {}
zz = []

logger.add('debug.log', format='{time} {level} {message}', level='DEBUG')

def send_telegram(text):
    token = "1832470032:AAH-RVl2FE6PeVmoVo6iR0OFnbcArNWtLg8"
    url = "https://api.telegram.org/bot"
    channel_id = "498516666"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

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
    commands = ['ZAKAZ','1', '1',  '1', '5', '1', '2']#, '1', '3']#, '3','Вавилова','1','25','0']
    # commands = ['ZAKAZ','1', '1',  '2', '3', '1', '3']#, '1', '3']#, '3','Вавилова','1','25','0']
    # # commands = ['ZAKAZ']
    # number_client = '79957745448'
    number_client = '77071392125'
    cx_test = len(commands)
    for c in commands:
          print('Command:',c)
          Body = {'typeWebhook': 'incomingMessageReceived',
                  'instanceData': {'idInstance': 9102, 'wid': '77717919485@c.us', 'typeInstance': 'whatsapp'},
                  'timestamp': 1616138603, 'idMessage': '3EB00939A99DB774DE89',
                  'senderData': {'chatId': number_client+'@c.us', 'sender': '77071392125@c.us', 'senderName': 'Юрич'},
                  'messageData': {'typeMessage': 'textMessage', 'textMessageData': {'textMessage': c}}}
          bot = WABot(Body, clients, logger)
          bot.processing(True)
          time.sleep(1)
    while True:
        c = input()
        Body = {'typeWebhook': 'incomingMessageReceived', 'instanceData': {'idInstance': 9102, 'wid': '77717919485@c.us', 'typeInstance': 'whatsapp'}, 'timestamp': 1616138603, 'idMessage': '3EB00939A99DB774DE89', 'senderData': {'chatId': number_client+'@c.us', 'sender': number_client+'@c.us', 'senderName': 'Юрич'}, 'messageData': {'typeMessage': 'textMessage', 'textMessageData': {'textMessage': c}}}
        bot = WABot(Body, clients, logger)
        bot.processing(True)
    # key = os.getenv('key')
    logger.info('Start')
    pid = os.getpid()
    send_telegram(f'pid from app: {str(pid)}')
    # # if key:
    # send_telegram(key)
    logger.info(f'pid from app: {str(pid)}')
    while True:
        logger.info('Step')
        # key = os.getenv('key')
        # if key:
        #     send_telegram('я мониторю..')
        json = get_notifications(token)
        if json == None:
            # print('нет ответа')
            continue
        receipt = json['receiptId']
        body = json['body']
        try:
            if body['messageData']['typeMessage'] == 'textMessage':
                logger.debug(body['messageData']['textMessageData']['textMessage'])
                bot = WABot(body, clients, logger)
                bot.processing()
        except Exception as ex:
            # errorText =  f" команда: {body['messageData']['textMessageData']['textMessage']} \n" + ex
            logger.error(ex)
            print(ex)
            send_telegram(ex)


        if receipt:
            del_notifications(token, receipt)


def write_pid(pid_file: str):
    with open(pid_file, mode="w", encoding="utf8") as file:
        file.write(f"{os.getpid()}")



if(__name__) == '__main__':
    write_pid('pid.pid')
    primera()
