from datetime import datetime, timedelta, timezone, date, time
import requests



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


def report_telegram():
    send_telegram('test cron')
    # data = TabluarOrders.objects.filter(order__client__driver=self, order__date_dev=datetime.date.today()).order_by('order__client__district')

if __name__ == '__main__':
    report_telegram()