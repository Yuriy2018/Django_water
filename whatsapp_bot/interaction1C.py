from requests.auth import HTTPBasicAuth
import requests
import json

user1C = 'admin'
pass1C = '777'
url1C = 'http://localhost:81/Almaz'

def get_client(number):
    myUrl =  url1C +'/hs/ChatBot/' + number
    headers = {'Content-Type': 'application/json', 'Accept-Encoding': None, 'Authorization': 'Basic'}
    auth = HTTPBasicAuth(user1C, pass1C)
    res = requests.get(myUrl, headers=headers, auth=auth)
    if res.text != '':
        return json.loads(res.text)

def get_data():
    myUrl =  url1C +'/hs/ChatBot/getdata'
    headers = {'Content-Type': 'application/json', 'Accept-Encoding': None, 'Authorization': 'Basic'}
    auth = HTTPBasicAuth(user1C, pass1C)
    res = requests.get(myUrl, headers=headers, auth=auth)
    if res.text != '':
        return json.loads(res.text).get('positions')


def get_zakaz_1c(data):
    data1C = {'name': data.name,
              'phone': data.id,
              'client': data.UID,
              # 'address': data.address,
              'date': data.date_of_delivery,
              'time': data.time_of_delivery,
              'payment': data.payment,
              'chatId': data.id,
              'cart': data.cart}

    myUrl = url1C + '/hs/ChatBot/addzakaz'
    headers = {'Content-Type': 'application/json', 'Accept-Encoding': None, 'Authorization': 'Basic'}
    auth = HTTPBasicAuth(user1C, pass1C)
    res = requests.post(myUrl, headers=headers, auth=auth, data=json.dumps(data1C))
    data.orders.append(res.text)
    return res

def get_last_zakaz_1c(number):

    # myUrl = url1C + f'/hs/ChatBot/lastcart/{number}'
    myUrl = url1C + f'/hs/ChatBot/lastcart/{number}'
    headers = {'Content-Type': 'application/json', 'Accept-Encoding': None, 'Authorization': 'Basic'}
    auth = HTTPBasicAuth(user1C, pass1C)
    res = requests.get(myUrl, headers=headers, auth=auth)
    if res.text != '':
        return json.loads(res.text)

def add_client_1c(data):
    data1C = {'name': data.name,
              'company': data.company,
              'contactPerson': data.contactPerson,
              'phoneContactPerson': data.phoneContactPerson,
              'phone': data.id,
              'client': data.UID,
              'area': data.district['district'],
              'driver': data.district['driver'],
              'street': data.street,
              'type': data.type,
              'number_home': data.number_home,
              'number_apart': data.number_apart,
              'chatId': data.id,
              }

    myUrl = url1C + '/hs/ChatBot/addclient'
    headers = {'Content-Type': 'application/json', 'Accept-Encoding': None, 'Authorization': 'Basic'}
    auth = HTTPBasicAuth(user1C, pass1C)
    res = requests.post(myUrl, headers=headers, auth=auth, data=json.dumps(data1C))
    data.UID = res.text
    return res