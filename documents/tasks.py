from datetime import datetime, timedelta, timezone, date, time
from celery import shared_task
import requests
from django.db.models import Sum, Count
from .models import Order, TabluarOrders


@shared_task
def add():
    print('Celery Cron работает')
    return True

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



@shared_task
def report_telegram():
    # currentdate = datetime.today()
    # start = currentdate.replace(hour=0, minute=0, second=0, microsecond=0,tzinfo=tzinfo.utc)
    # finish = currentdate.replace(hour=23, minute=59, second=59, microsecond=0,tzinfo='UTC')
    # start = datetime.strptime('24/07/2021', "%d/%m/%Y")
    # finish = datetime.strptime('24/07/2021', "%d/%m/%Y") + timedelta(days=1)
    start = datetime.combine(date.today(), time(00, 00, 00))  # Начало дня
    finish = datetime.combine(date.today(), time(23, 59, 59))  # Конец дня
    data = TabluarOrders.objects.filter(order__date__gte=start, order__date__lte=finish).aggregate(total=Sum('amount'))
    # tab = TabluarOrders.objects.filter(order__date__gte=start, order__date__lte=finish).order_by('driver', 'district')

    print(data)
    str_report = f'Текущая сумма заказов за день: {str(data["total"])}'
    send_telegram(str_report)
    return str_report
    # data = TabluarOrders.objects.filter(order__client__driver=self, order__date_dev=datetime.date.today()).order_by('order__client__district')
