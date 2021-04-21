import requests
# import requests
from urllib import request
from requests.auth import HTTPBasicAuth
import json
def get_notifications(token):
    url = "https://api.green-api.com/waInstance9102/ReceiveNotification/710d9d92265ba34c1c8be98f5e490aafa63968a97c3b5caa5d"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.text:
        return response.json()

def del_notifications(token,receipt):
    url = "https://api.green-api.com/waInstance9102/DeleteNotification/710d9d92265ba34c1c8be98f5e490aafa63968a97c3b5caa5d/" + str(receipt)

    payload = {}
    headers = {}

    response = requests.request("DELETE", url, headers=headers, data=payload)

    print(response.text.encode('utf8'))



def reset_calls(token):
    json = get_notifications(token)
    # json = get_notificationsQR(tokenQR)
    if json == None:
        return 'clear'

    receipt = json['receiptId']
    if receipt:
        del_notifications(token, receipt)

if __name__ == '__main__':
    # myUrl = 'http://localhost:80/base/hs/status/7058370045'
    # headers = {'Content-Type': 'application/json', 'Accept-Encoding': None, 'Authorization': 'Basic'}
    # auth = HTTPBasicAuth('AdminBot', '777')
    # res = requests.get(myUrl, headers=headers, auth=auth)
    # listStatus = json.loads(res.text)
    # t = ''
    # if len(listStatus) == 0:
    #     t = 'Заказы за текущий день не найдены!'
    # elif len(listStatus) == 1:
    #     t = f'Статус заказа - {listStatus[0]["Status"]}'
    # else:
    #     for cx,sts in enumerate(listStatus):
    #         t += f'{cx+1}. Заказ на сумму: {sts["Summa"]} статус - {sts["Status"]} \n'
    #
    # print(t)
    token = 'gr.eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50SWQiOjIyODM2MjEyLCJhY2NvdW50IjoxMzg2LCJleHAiOjQ3NTk5Njk2MDN9.m0LWeTmSeMSoC_NQrNPDvxZxpDwwgISjn0-SNYkJU_o'
    while True:
      aa = reset_calls(token)
      print('***')
      if aa == 'clear':
          break
          pritn('finish')
