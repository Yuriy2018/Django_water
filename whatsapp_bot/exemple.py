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


import requests
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

if __name__ == '__main__':

  while True:
    currend_date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    send_telegram(currend_date)
    time.sleep(600)
