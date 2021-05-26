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
    commands = ['ZAKAZ','1', '1',  '2', '1']#, '1', '1']#, '1', '3']#, '3','Вавилова','1','25','0']
    # commands = ['ZAKAZ']
    number_client = '77071392150'
    # cx_test = len(commands)
    for c in commands:
          print('Command:',c)
          Body = {'typeWebhook': 'incomingMessageReceived',
                  'instanceData': {'idInstance': 9102, 'wid': '77717919485@c.us', 'typeInstance': 'whatsapp'},
                  'timestamp': 1616138603, 'idMessage': '3EB00939A99DB774DE89',
                  'senderData': {'chatId': number_client+'@c.us', 'sender': '77071392125@c.us', 'senderName': 'Юрич'},
                  'messageData': {'typeMessage': 'textMessage', 'textMessageData': {'textMessage': c}}}
          bot = WABot(Body, clients, conn)
          bot.processing(True)
          time.sleep(1)
    while True:
        c = input()
        Body = {'typeWebhook': 'incomingMessageReceived', 'instanceData': {'idInstance': 9102, 'wid': '77717919485@c.us', 'typeInstance': 'whatsapp'}, 'timestamp': 1616138603, 'idMessage': '3EB00939A99DB774DE89', 'senderData': {'chatId': number_client+'@c.us', 'sender': number_client+'@c.us', 'senderName': 'Юрич'}, 'messageData': {'typeMessage': 'textMessage', 'textMessageData': {'textMessage': c}}}
        bot = WABot(Body, clients, conn)
        bot.processing(True)

    while True:

        json = get_notifications(token)
        if json == None:
            # print('нет ответа')
            continue

        receipt = json['receiptId']
        body = json['body']
        try:
            if body['messageData']['typeMessage'] == 'textMessage':
                bot = WABot(body, clients, conn)
                bot.processing()
        except Exception as ex:
            print(ex)

        # for ntfc in notifications['messageDate']:
        #
        #     if ntfc['messages'][0]['type'] != 'text':
        #         continue
        #
        #     body = ntfc['messages'][0]['text']['body']
        #     # time.time()
        #     print("Команда: ",body)
        #     bot = WABot(ntfc, clients, conn)
        #     bot.processing()
            # print(body)

        if receipt:
            del_notifications(token, receipt)


# def get_zakaz_1c(pay):

    # cartOb = ast.literal_eval(pay['cart'])
    # data1C = {'name': pay['name'],
    #           'phone': pay['phone'],
    #           'address': pay['address'],
    #           'time': pay['time_of_delivery'],
    #           'note': pay['note'],
    #           'payment': 'безналичная оплата',
    #           'chatId': pay['phone'],
    #           'cart': cartOb,
    #           }
    # myUrl = 'http://localhost:81/SS/hs/ftotest/555'
    # headers = {'Content-Type': 'application/json', 'Accept-Encoding': None, 'Authorization': 'Basic'}
    # auth = HTTPBasicAuth('admin', '777')
    # res = requests.post(myUrl, headers=headers, auth=auth, data=json.dumps(data1C))
    # return res

def acces_pay(numberPay,number1C):
    # q = """
    #     UPDATE orders SET paid, number1C WHERE numberPay ={numberPay}
    #     """.format(p=1, numberPay=numberPay, number1C=number1C)
    # cursor.execute(q)
    # cursor.execute('''UPDATE orders SET (paid=?,number1C=?) WHERE numberPay=?''',(1, number1C, numberPay))


    sql_update_query = """Update orders set paid = ?, number1C=?  where numberPay = ?"""
    data = (1, number1C, numberPay)
    cursor.execute(sql_update_query, data)
    conn.commit()


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
