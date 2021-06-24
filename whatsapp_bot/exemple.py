# from requests.auth import HTTPBasicAuth
# import requests
# url = "https://water.hostman.site/api/get_orders1c/"
# auth = HTTPBasicAuth('admin','123')
# r = requests.get(url=url)
#
#
# f = requests.get(url, auth=HTTPBasicAuth('yuriy', '123'))
#
#
# resp = requests.post('http://127.0.0.1:8000/login/', {'username': 'akshar', 'password': 'abc'})


import requests, json
import datetime
import time

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

    if r.status_code != 200:
        raise Exception("post_text error")

def get_out():
    url = "https://api.green-api.com/waInstance7948/lastOutgoingMessages/7c6a91b25c8e0d1a14bce0b7118d76668bc5e2dddc06ac9783"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    dataJ = json.loads(response.text.encode('utf8'))
    outgoing = set()
    for dt in dataJ:
        outgoing.add(dt['chatId'].replace('@c.us', ''))
    print(dataJ)

def add_client(number_phone, address):
    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "name": address,
        "address": address,
        "phone_number": number_phone,
    }
    api_url = 'http://127.0.0.1:8000'
    response = requests.request("POST", api_url + '/api/add_client/', headers=headers, data=json.dumps(payload))

    return json.loads(response.text)
if __name__ == '__main__':

    text = '''Здравствуйте! Примите заявку на воду. Код на воротах 29; код на подъезде 34.
    1 бутыль'''
    res = add_client('77071397775',text)
    get_out()
  # while True:
  #   currend_date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
  #   send_telegram(currend_date)
  #   time.sleep(600)
