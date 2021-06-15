import subprocess
import time

import psutil

import requests

def run_process():
     p = subprocess.Popen(['/usr/bin/python3', 'app.py'])
     return p

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


if(__name__) == '__main__':
    proc = run_process()
    pid = proc.pid

    while True:
        time.sleep(60)
        if not psutil.pid_exists(pid):
            proc = run_process()
            pid = proc.pid
            send_telegram(f'Автоматический перезапуск pid: {pid}')
