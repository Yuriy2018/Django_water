import time, datetime, redis, requests, json

APIUrl = 'https://api.green-api.com/waInstance7948/'
token = '7c6a91b25c8e0d1a14bce0b7118d76668bc5e2dddc06ac9783'

r = redis.Redis(host='45.147.176.206', port=6379, db=0)


text_buzzy = "Для продолжения заказа нажмите 1 или Ваш заказ останется не принятым! \nЛибо свяжитесь с оператором по номеру:+7 708 471 3855(whatsapp)"


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

def process_buzzy():
    '''Процедура выполняет проверку чатов, где клиент написал первое сообщение и не стал
    реагировать на команды бота
    '''
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
                   send_text(number,text_buzzy)
                   print(number)
                   r.hdel('buzzy',i)

        else:
            time.sleep(290)

if __name__ == '__main__':
    process_buzzy()
