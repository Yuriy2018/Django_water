import time
from wabot_Almaz_mini import is_server, APIUrl, token
import requests, redis, json, datetime
from threading import Thread

if is_server:
    r = redis.Redis(host='45.147.176.206', port=6379, db=0)
else:
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)

text_buzzy = "Для продолжения заказа нажмите 1 или Ваш заказ останется не принятым! \nЛибо свяжитесь с оператором по номеру:+7 708 471 3855(whatsapp)\nЗвонки принимаются до 17:30"


def send_text(phone, text):
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


def supervisor(send_telegramM, sleep):
    """ Проверяем, активен ли основной скрипт бота, если нет, то шлем предупреждение в телеграмм"""
    print('запущен Supervisor')
    prim = False
    while True:
        if r.get('active') is None:
            if prim:
                send_telegramM(f"Внимание, бот молчит! Проверьте скрипт!")
            else:
                prim = True
        else:
            prim = False
        sleep(10)


def buzzy():
    """Сканируем тех клиентов, кто написал первое сообщение и больше не ответил"""
    print('запущен Buzzy')
    while True:
        time.sleep(10)
        res = r.hgetall('buzzy')
        if res:
            for i in res:
                cur_unix = int(datetime.datetime.now().timestamp())
                cur_time = int(res[i])
                if cur_unix - cur_time > 300:
                    number = i.decode('utf-8')
                    send_text(number, text_buzzy)
                    print("Отправка сообщения!", number)
                    r.hdel('buzzy', i)

        else:
            time.sleep(290)


if (__name__) == '__main__':
    t1 = Thread(target=supervisor, args=(send_telegram, time.sleep))
    t2 = Thread(target=buzzy)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
